"""
Comparative Benchmarking Pipeline across 4 Model Families for GLOF Prediction:
  1. Random Forest / Tree Baseline
  2. Multi-Task LSTM (Recurrent Network)
  3. Multi-Task TCN (1D Causal Dilated Conv)
  4. Multi-Task DLinear (Trend-Seasonal Decomposition)

Evaluates:
  - Lake Surface Area Forecasting Accuracy (R2, RMSE km2, MAE km2)
  - Critical GLOF Hazard Alert Detection (Accuracy %, Macro F1-Score)
"""

import os
import time
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, accuracy_score, f1_score

from data.prepare_glof_dataset import GLOFDataModule, TORCH_AVAILABLE
from models.xgboost_baseline import GLOFTreeBaseline

if TORCH_AVAILABLE:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from models.lstm_glof import GLOFLSTM
    from models.tcn_glof import GLOFTCN
    from models.dlinear_glof import GLOFDLinear

def train_multitask_pytorch(model, train_loader, val_loader, epochs=35, lr=0.002, device="cpu"):
    model.to(device)
    crit_reg = nn.MSELoss()
    crit_cls = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    best_loss = float('inf')
    best_weights = None

    for ep in range(1, epochs + 1):
        model.train()
        for xb, y_reg, y_cls in train_loader:
            xb, y_reg, y_cls = xb.to(device), y_reg.to(device), y_cls.to(device)
            optimizer.zero_grad()
            pred_area, risk_logits = model(xb)
            loss = crit_reg(pred_area, y_reg) + 0.5 * crit_cls(risk_logits, y_cls)
            loss.backward()
            optimizer.step()

        # Validation
        model.eval()
        vloss = 0.0
        with torch.no_grad():
            for xb, y_reg, y_cls in val_loader:
                xb, y_reg, y_cls = xb.to(device), y_reg.to(device), y_cls.to(device)
                pred_area, risk_logits = model(xb)
                l = crit_reg(pred_area, y_reg) + 0.5 * crit_cls(risk_logits, y_cls)
                vloss += l.item() * len(xb)
        vloss /= len(val_loader.dataset)

        if vloss < best_loss:
            best_loss = vloss
            best_weights = model.state_dict().copy()

    if best_weights is not None:
        model.load_state_dict(best_weights)
    return model

def run_glof_benchmark(csv_path=None, epochs=35, output_csv="glof_comparative_metrics.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if csv_path is None:
        csv_path = os.path.join(script_dir, "data", "himalayan_glacial_lakes_2015_2024.csv")

    print("=" * 75)
    print("  GLACIAL LAKE EXPANSION & GLOF HAZARD PREDICTION BENCHMARK (2015–2024)")
    print("=" * 75)

    dm = GLOFDataModule(csv_path, lookback=6, horizon=1)
    dm.build_windows()
    y_test_unscaled = dm.test_y_unscaled.ravel()
    y_test_cls = dm.test_y_cls

    results = []
    device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
    print(f"Using compute device: {device}\n")

    # 1. Random Forest Baseline
    print("Training Model 1: Random Forest (Baseline)...")
    t0 = time.time()
    rf = GLOFTreeBaseline(n_estimators=100, max_depth=10)
    rf.fit(dm.train_X_s, dm.train_y_s, dm.train_y_cls)
    rf_area_scaled = rf.predict_area(dm.test_X_s)
    rf_area = dm.target_scaler.inverse_transform(rf_area_scaled.reshape(-1, 1)).ravel()
    rf_risk = rf.predict_risk(dm.test_X_s)
    t_rf = round(time.time() - t0, 2)

    results.append({
        "Model": "Random Forest",
        "Area_R2": round(float(r2_score(y_test_unscaled, rf_area)), 4),
        "Area_RMSE_km2": round(float(np.sqrt(mean_squared_error(y_test_unscaled, rf_area))), 4),
        "Area_MAE_km2": round(float(mean_absolute_error(y_test_unscaled, rf_area)), 4),
        "Risk_Accuracy_pct": round(float(accuracy_score(y_test_cls, rf_risk) * 100.0), 2),
        "Risk_F1_Macro": round(float(f1_score(y_test_cls, rf_risk, average='macro')), 4),
        "Time_s": t_rf
    })
    print(f"  -> R2: {results[-1]['Area_R2']} | RMSE: {results[-1]['Area_RMSE_km2']} km2 | Alert Acc: {results[-1]['Risk_Accuracy_pct']}% ({t_rf}s)")

    if not TORCH_AVAILABLE:
        print("\nNote: PyTorch not installed locally. Deep learning models can be trained on Colab.")
        df_res = pd.DataFrame(results)
        df_res.to_csv(os.path.join(script_dir, output_csv), index=False)
        return df_res

    # 2. Multi-Task LSTM
    print("\nTraining Model 2: Multi-Task LSTM...")
    t0 = time.time()
    lstm = GLOFLSTM(input_dim=7, hidden_dim=64, num_layers=2)
    lstm = train_multitask_pytorch(lstm, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    t_lstm = round(time.time() - t0, 2)

    lstm.eval()
    with torch.no_grad():
        p_area, p_risk = lstm(torch.from_numpy(dm.test_X_s).to(device))
        lstm_area = dm.target_scaler.inverse_transform(p_area.cpu().numpy()).ravel()
        lstm_risk = torch.argmax(p_risk, dim=1).cpu().numpy()

    results.append({
        "Model": "LSTM",
        "Area_R2": round(float(r2_score(y_test_unscaled, lstm_area)), 4),
        "Area_RMSE_km2": round(float(np.sqrt(mean_squared_error(y_test_unscaled, lstm_area))), 4),
        "Area_MAE_km2": round(float(mean_absolute_error(y_test_unscaled, lstm_area)), 4),
        "Risk_Accuracy_pct": round(float(accuracy_score(y_test_cls, lstm_risk) * 100.0), 2),
        "Risk_F1_Macro": round(float(f1_score(y_test_cls, lstm_risk, average='macro')), 4),
        "Time_s": t_lstm
    })
    print(f"  -> R2: {results[-1]['Area_R2']} | RMSE: {results[-1]['Area_RMSE_km2']} km2 | Alert Acc: {results[-1]['Risk_Accuracy_pct']}% ({t_lstm}s)")

    # 3. Multi-Task TCN
    print("\nTraining Model 3: Multi-Task TCN...")
    t0 = time.time()
    tcn = GLOFTCN(input_dim=7, num_channels=[32, 64], kernel_size=2)
    tcn = train_multitask_pytorch(tcn, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    t_tcn = round(time.time() - t0, 2)

    tcn.eval()
    with torch.no_grad():
        p_area, p_risk = tcn(torch.from_numpy(dm.test_X_s).to(device))
        tcn_area = dm.target_scaler.inverse_transform(p_area.cpu().numpy()).ravel()
        tcn_risk = torch.argmax(p_risk, dim=1).cpu().numpy()

    results.append({
        "Model": "TCN",
        "Area_R2": round(float(r2_score(y_test_unscaled, tcn_area)), 4),
        "Area_RMSE_km2": round(float(np.sqrt(mean_squared_error(y_test_unscaled, tcn_area))), 4),
        "Area_MAE_km2": round(float(mean_absolute_error(y_test_unscaled, tcn_area)), 4),
        "Risk_Accuracy_pct": round(float(accuracy_score(y_test_cls, tcn_risk) * 100.0), 2),
        "Risk_F1_Macro": round(float(f1_score(y_test_cls, tcn_risk, average='macro')), 4),
        "Time_s": t_tcn
    })
    print(f"  -> R2: {results[-1]['Area_R2']} | RMSE: {results[-1]['Area_RMSE_km2']} km2 | Alert Acc: {results[-1]['Risk_Accuracy_pct']}% ({t_tcn}s)")

    # 4. Multi-Task DLinear
    print("\nTraining Model 4: Multi-Task DLinear...")
    t0 = time.time()
    dlinear = GLOFDLinear(lookback=6, input_dim=7)
    dlinear = train_multitask_pytorch(dlinear, dm.train_loader, dm.val_loader, epochs=epochs, device=device)
    t_dlin = round(time.time() - t0, 2)

    dlinear.eval()
    with torch.no_grad():
        p_area, p_risk = dlinear(torch.from_numpy(dm.test_X_s).to(device))
        dlinear_area = dm.target_scaler.inverse_transform(p_area.cpu().numpy()).ravel()
        dlinear_risk = torch.argmax(p_risk, dim=1).cpu().numpy()

    results.append({
        "Model": "DLinear",
        "Area_R2": round(float(r2_score(y_test_unscaled, dlinear_area)), 4),
        "Area_RMSE_km2": round(float(np.sqrt(mean_squared_error(y_test_unscaled, dlinear_area))), 4),
        "Area_MAE_km2": round(float(mean_absolute_error(y_test_unscaled, dlinear_area)), 4),
        "Risk_Accuracy_pct": round(float(accuracy_score(y_test_cls, dlinear_risk) * 100.0), 2),
        "Risk_F1_Macro": round(float(f1_score(y_test_cls, dlinear_risk, average='macro')), 4),
        "Time_s": t_dlin
    })
    print(f"  -> R2: {results[-1]['Area_R2']} | RMSE: {results[-1]['Area_RMSE_km2']} km2 | Alert Acc: {results[-1]['Risk_Accuracy_pct']}% ({t_dlin}s)")

    df_res = pd.DataFrame(results)
    out_file = os.path.join(script_dir, output_csv)
    df_res.to_csv(out_file, index=False)
    print("\n" + "=" * 75)
    print("  FINAL GLOF BENCHMARK RESULTS")
    print("=" * 75)
    print(df_res.to_string(index=False))
    print(f"\nSaved benchmark metrics to: {out_file}")
    return df_res

if __name__ == "__main__":
    run_glof_benchmark()

