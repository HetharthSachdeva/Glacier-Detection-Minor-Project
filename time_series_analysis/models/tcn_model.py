"""
Model 3: Temporal Convolutional Network (TCN)
----------------------------------------------
Based on Bai et al. (2018): "An Empirical Evaluation of Generic Convolutional 
and Recurrent Networks for Sequence Modeling".

Key Features:
  1. Causal Convolutions: Strict temporal causality (no future leakage).
  2. Dilated Convolutions: Exponentially large receptive field across decades.
  3. Residual Connections: Stabilizes deep gradient flow.
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
        """Removes the trailing padding elements to enforce causal convolution."""
        def __init__(self, chomp_size):
            super(Chomp1d, self).__init__()
            self.chomp_size = chomp_size

        def forward(self, x):
            return x[:, :, :-self.chomp_size].contiguous() if self.chomp_size > 0 else x

    class TemporalBlock(nn.Module):
        def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
            super(TemporalBlock, self).__init__()
            self.conv1 = nn.Conv1d(n_inputs, n_outputs, kernel_size,
                                   stride=stride, padding=padding, dilation=dilation)
            self.chomp1 = Chomp1d(padding)
            self.relu1 = nn.ReLU()
            self.dropout1 = nn.Dropout(dropout)

            self.conv2 = nn.Conv1d(n_outputs, n_outputs, kernel_size,
                                   stride=stride, padding=padding, dilation=dilation)
            self.chomp2 = Chomp1d(padding)
            self.relu2 = nn.ReLU()
            self.dropout2 = nn.Dropout(dropout)

            self.net = nn.Sequential(
                self.conv1, self.chomp1, self.relu1, self.dropout1,
                self.conv2, self.chomp2, self.relu2, self.dropout2
            )
            self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
            self.relu = nn.ReLU()

        def forward(self, x):
            out = self.net(x)
            res = x if self.downsample is None else self.downsample(x)
            return self.relu(out + res)

    class GlacierTCN(nn.Module):
        def __init__(self, input_dim=7, num_channels=[32, 64], kernel_size=2, output_dim=1, dropout=0.2):
            super(GlacierTCN, self).__init__()
            layers = []
            num_levels = len(num_channels)
            for i in range(num_levels):
                dilation_size = 2 ** i
                in_channels = input_dim if i == 0 else num_channels[i-1]
                out_channels = num_channels[i]
                padding = (kernel_size - 1) * dilation_size
                layers += [TemporalBlock(in_channels, out_channels, kernel_size, stride=1,
                                         dilation=dilation_size, padding=padding, dropout=dropout)]

            self.network = nn.Sequential(*layers)
            self.linear = nn.Linear(num_channels[-1], output_dim)

        def forward(self, x):
            # Input x: (Batch, Lookback, Features) -> Conv1d expects (Batch, Features, Lookback)
            x_conv = x.transpose(1, 2)
            y = self.network(x_conv)
            # Take the output at the final temporal time step
            out = self.linear(y[:, :, -1])
            return out
else:
    class GlacierTCN:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required to use GlacierTCN.")

