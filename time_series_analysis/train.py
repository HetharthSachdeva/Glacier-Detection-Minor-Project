"""
Comparative Training & Benchmarking Pipeline across 4 Time-Series Model Families:
  1. Random Forest (Classical Baseline)
  2. LSTM (Recurrent Sequence Model)
  3. TCN (Temporal 1D Dilated Convolutional Network)
  4. DLinear (Trend-Seasonal Decomposition Linear Model)

Outputs:
  - comparative_forecast_metrics.csv
  - Checkpoint weights in time_series_analysis/checkpoints/
"""

import os
import time
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from data.prepare_dataset import GlacierTimeSeriesDataModule, TORCH_AVAILABLE
from models.random_forest import GlacierRandomForest

if TORCH_AVAILABLE:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from models.lstm_model import GlacierLSTM
    from models.tcn_model import GlacierTCN
    from models.dlinear_model import GlacierDLinear

def calculate_mape(y_true, y_pred, eps=1e-6):
    """Mean Absolute Percentage Error (%)"""
    return np.mean(np.abs((y_true - y_pred) / (y_true + eps))) * 100.0

def train_pytorch_model(model, train_loader, val_loader, epochs=40, lr=0.002, device="cpu"):
    """Generic lightweight training loop for PyTorch time-series models."""
    model.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

    best_val_loss = float('inf')
    best_weights = None

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            preds = model(X_batch)
            loss = criterion(preds, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(X_batch)

        train_loss /= len(train_loader.dataset)

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_val, y_val in val_loader:
                X_val, y_val = X_val.to(device), y_val.to(device)
                preds = model(X_val)
                loss = criterion(preds, y_val)
                val_loss += loss.item() * len(X_val)

        val_loss /= len(val_loader.dataset)
        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = model.state_dict().copy()

    # Restore best checkpoint
    if best_weights is not None:
        model.load_state_dict(best_weights)
    return model

def evaluate_model(y_true_km2, y_pred_km2):
    r2 = r2_score(y_true_km2, y_pred_km2)
    rmse = np.sqrt(mean_squared_error(y_true_km2, y_pred_km2))
    mae = mean_absolute_error(y_true_km2, y_pred_km2)
    mape = calculate_mape(y_true_km2, y_pred_km2)
    return {
        "R2_Score": round(float(r2), 4),
        "RMSE_km2": round(float(rmse), 4),
        "MAE_km2": round(float(mae), 4),
        "MAPE_pct": round(float(mape), 2)
    }

def run_comparative_benchmark(csv_path=None, epochs=40, output_csv="comparative_forecast_metrics.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if csv_path is None:
        csv_path = os.path.join(script_dir, "data", "ladakh_glaciers_2000_2024.csv")

    print("=" * 70)
    print("  GLACIER RETREAT TIME-SERIES COMPARATIVE BENCHMARK (2000 - 2024)")
    print("=" * 70)

    # 1. Prepare Data
    dm = GlacierTimeSeriesDataModule(csv_path, lookback=5, horizon=1)
    dm.build_windows()
    y_test_km2 = dm.test_y_unscaled.ravel()

    results = []
    device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
    print(f"Using compute device: {device}\n")

    # -------------------------------------------------------------
    # MODEL 1: Random Forest Regressor
    # -------------------------------------------------------------
    print("Training Model 1: Random Forest (Baseline)...")
    t0 = time.time()
    rf = GlacierRandomForest(n_estimators=100, max_depth=10)
    rf.fit(dm.rf_train_X, dm.rf_train_y)
    rf_pred = rf.predict(dm.rf_test_X)
    rf_time = round(time.time() - t0, 2)
    
    rf_metrics = evaluate_model(y_test_km2, rf_pred)
    rf_metrics.update({"Model": "Random Forest", "Training_Time_s": rf_time, "Params": "N/A"})
    results.append(rf_metrics)
    print(f"  -> R2: {rf_metrics['R2_Score']} | RMSE: {rf_metrics['RMSE_km2']} km2 | MAE: {rf_metrics['MAE_km2']} km2 ({rf_time}s)")

    if not TORCH_AVAILABLE:
        print("\nNote: PyTorch not installed locally. Deep learning models can be trained on Google Colab.")
        df_res = pd.DataFrame(results)
        df_res.to_csv(os.path.join(script_dir, output_csv), index=False)
        return df_res

    # -------------------------------------------------------------
    # MODEL 2: Long Short-Term Memory (LSTM)
    # -------------------------------------------------------------
    print("\nTraining Model 2: LSTM (Recurrent Network)...")
    t0 = time.time()
    lstm = GlacierLSTM(input_dim=7, hidden_dim=64, num_layers=2, output_dim=1)
    lstm = train_pytorch_model(lstm, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    lstm_time = round(time.time() - t0, 2)

    lstm.eval()
    with torch.no_grad():
        preds_scaled = lstm(torch.from_numpy(dm.test_X_scaled).float().to(device)).cpu().numpy()
        lstm_pred = dm.target_scaler.inverse_transform(preds_scaled).ravel()

    lstm_params = sum(p.numel() for p in lstm.parameters())
    lstm_metrics = evaluate_model(y_test_km2, lstm_pred)
    lstm_metrics.update({"Model": "LSTM", "Training_Time_s": lstm_time, "Params": f"{lstm_params:,}"})
    results.append(lstm_metrics)
    print(f"  -> R2: {lstm_metrics['R2_Score']} | RMSE: {lstm_metrics['RMSE_km2']} km2 | MAE: {lstm_metrics['MAE_km2']} km2 ({lstm_time}s)")

    # -------------------------------------------------------------
    # MODEL 3: Temporal Convolutional Network (TCN)
    # -------------------------------------------------------------
    print("\nTraining Model 3: Temporal Convolutional Network (TCN)...")
    t0 = time.time()
    tcn = GlacierTCN(input_dim=7, num_channels=[32, 64], kernel_size=2, output_dim=1)
    tcn = train_pytorch_model(tcn, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    tcn_time = round(time.time() - t0, 2)

    tcn.eval()
    with torch.no_grad():
        preds_scaled = tcn(torch.from_numpy(dm.test_X_scaled).float().to(device)).cpu().numpy()
        tcn_pred = dm.target_scaler.inverse_transform(preds_scaled).ravel()

    tcn_params = sum(p.numel() for p in tcn.parameters())
    tcn_metrics = evaluate_model(y_test_km2, tcn_pred)
    tcn_metrics.update({"Model": "TCN", "Training_Time_s": tcn_time, "Params": f"{tcn_params:,}"})
    results.append(tcn_metrics)
    print(f"  -> R2: {tcn_metrics['R2_Score']} | RMSE: {tcn_metrics['RMSE_km2']} km2 | MAE: {tcn_metrics['MAE_km2']} km2 ({tcn_time}s)")

    # -------------------------------------------------------------
    # MODEL 4: DLinear (Trend-Seasonal Decomposition)
    # -------------------------------------------------------------
    print("\nTraining Model 4: DLinear (Decomposition Linear Model)...")
    t0 = time.time()
    dlinear = GlacierDLinear(lookback=5, input_dim=7, output_dim=1, kernel_size=3)
    dlinear = train_pytorch_model(dlinear, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    dlinear_time = round(time.time() - t0, 2)

    dlinear.eval()
    with torch.no_grad():
        preds_scaled = dlinear(torch.from_numpy(dm.test_X_scaled).float().to(device)).cpu().numpy()
        dlinear_pred = dm.target_scaler.inverse_transform(preds_scaled).ravel()

    dlinear_params = sum(p.numel() for p in dlinear.parameters())
    dlinear_metrics = evaluate_model(y_test_km2, dlinear_pred)
    dlinear_metrics.update({"Model": "DLinear", "Training_Time_s": dlinear_time, "Params": f"{dlinear_params:,}"})
    results.append(dlinear_metrics)
    print(f"  -> R2: {dlinear_metrics['R2_Score']} | RMSE: {dlinear_metrics['RMSE_km2']} km2 | MAE: {dlinear_metrics['MAE_km2']} km2 ({dlinear_time}s)")

    # -------------------------------------------------------------
    # Save & Summarize Benchmark
    # -------------------------------------------------------------
    df_res = pd.DataFrame(results)[["Model", "R2_Score", "RMSE_km2", "MAE_km2", "MAPE_pct", "Training_Time_s", "Params"]]
    out_file = os.path.join(script_dir, output_csv)
    df_res.to_csv(out_file, index=False)
    print("\n" + "=" * 70)
    print("  FINAL TIME-SERIES BENCHMARK RESULTS")
    print("=" * 70)
    print(df_res.to_string(index=False))
    print(f"\nSaved metrics to: {out_file}")
    return df_res

if __name__ == "__main__":
    run_comparative_benchmark()

