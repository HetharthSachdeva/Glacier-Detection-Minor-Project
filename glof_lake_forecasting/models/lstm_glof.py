"""
Model 2: Multi-Task LSTM Network for GLOF Prediction
-----------------------------------------------------
Ingests multi-temporal sequences of lake area, radar backscatter, and climate drivers.
Features dual prediction heads:
  1. Regression Head: Continuous forecast of next month's lake area (km2).
  2. Classification Head: GLOF Alert Risk Tier (0 = Low, 1 = Moderate, 2 = Critical).
"""

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    nn = object

if TORCH_AVAILABLE:
    class GLOFLSTM(nn.Module):
        def __init__(self, input_dim=7, hidden_dim=64, num_layers=2, num_classes=3, dropout=0.2):
            super(GLOFLSTM, self).__init__()
            self.lstm = nn.LSTM(
                input_size=input_dim,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                dropout=dropout if num_layers > 1 else 0.0
            )
            # Regression Head (Future Lake Area km2)
            self.area_head = nn.Sequential(
                nn.Linear(hidden_dim, 32),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(32, 1)
            )
            # Classification Head (GLOF Risk Tier 0, 1, 2)
            self.risk_head = nn.Sequential(
                nn.Linear(hidden_dim, 32),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(32, num_classes)
            )

        def forward(self, x):
            # x shape: (Batch, Lookback, Features)
            lstm_out, _ = self.lstm(x)
            last_step = lstm_out[:, -1, :]
            pred_area = self.area_head(last_step)
            risk_logits = self.risk_head(last_step)
            return pred_area, risk_logits
else:
    class GLOFLSTM:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for GLOFLSTM.")

