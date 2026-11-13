"""
Model 2: Long Short-Term Memory (LSTM / Bi-LSTM) Network
---------------------------------------------------------
A recurrent neural network with gated memory cells (Forget, Input, Output gates)
designed to learn multi-year temporal dependencies and climate-driven melt trends.
"""

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    nn = object

if TORCH_AVAILABLE:
    class GlacierLSTM(nn.Module):
        def __init__(self, input_dim=7, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2, bidirectional=False):
            super(GlacierLSTM, self).__init__()
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            self.bidirectional = bidirectional
            
            self.lstm = nn.LSTM(
                input_size=input_dim,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                dropout=dropout if num_layers > 1 else 0.0,
                bidirectional=bidirectional
            )
            
            fc_in = hidden_dim * 2 if bidirectional else hidden_dim
            self.head = nn.Sequential(
                nn.Linear(fc_in, 32),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(32, output_dim)
            )

        def forward(self, x):
            # x shape: (Batch, Lookback, Features)
            lstm_out, _ = self.lstm(x)
            # Take the representation at the final lookback year
            last_step = lstm_out[:, -1, :]
            out = self.head(last_step)
            return out
else:
    class GlacierLSTM:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required to use GlacierLSTM.")

