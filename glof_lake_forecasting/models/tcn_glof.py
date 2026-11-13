"""
Model 3: Temporal Convolutional Network (TCN) for GLOF Prediction
------------------------------------------------------------------
Uses 1D dilated causal convolutions with exponential receptive field expansion
to model multi-temporal lake expansion and dam vulnerability in parallel.
"""

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    nn = object

if TORCH_AVAILABLE:
    class Chomp1d(nn.Module):
        def __init__(self, chomp_size):
            super().__init__()
            self.chomp_size = chomp_size

        def forward(self, x):
            return x[:, :, :-self.chomp_size].contiguous() if self.chomp_size > 0 else x

    class TemporalBlock(nn.Module):
        def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv1d(n_inputs, n_outputs, kernel_size, stride=stride, padding=padding, dilation=dilation),
                Chomp1d(padding),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Conv1d(n_outputs, n_outputs, kernel_size, stride=stride, padding=padding, dilation=dilation),
                Chomp1d(padding),
                nn.ReLU(),
                nn.Dropout(dropout)
            )
            self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
            self.relu = nn.ReLU()

        def forward(self, x):
            out = self.net(x)
            res = x if self.downsample is None else self.downsample(x)
            return self.relu(out + res)

    class GLOFTCN(nn.Module):
        def __init__(self, input_dim=7, num_channels=[32, 64], kernel_size=2, num_classes=3, dropout=0.2):
            super().__init__()
            layers = []
            for i in range(len(num_channels)):
                d = 2 ** i
                in_ch = input_dim if i == 0 else num_channels[i-1]
                out_ch = num_channels[i]
                pad = (kernel_size - 1) * d
                layers.append(TemporalBlock(in_ch, out_ch, kernel_size, 1, d, pad, dropout))
            
            self.network = nn.Sequential(*layers)
            self.area_head = nn.Linear(num_channels[-1], 1)
            self.risk_head = nn.Linear(num_channels[-1], num_classes)

        def forward(self, x):
            # Input x: (Batch, Lookback, Features) -> Conv1d expects (Batch, Features, Lookback)
            y = self.network(x.transpose(1, 2))
            last_feat = y[:, :, -1]
            return self.area_head(last_feat), self.risk_head(last_feat)
else:
    class GLOFTCN:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for GLOFTCN.")

