"""
Model 4: DLinear (Trend-Seasonal Decomposition Linear Model)
------------------------------------------------------------
Based on Zeng et al. (AAAI 2023): "Are Transformers Effective for Time Series?"

Key Concept:
  Decomposes multi-variate time series into:
    1. Trend component (steady multi-year melting trend).
    2. Seasonal / Residual component (interannual climate fluctuations).
  Applies linear projections to each component independently, outperforming
  complex Transformers on physical data with zero risk of overfitting.
"""

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    nn = object

if TORCH_AVAILABLE:
    class SeriesDecomp(nn.Module):
        """Series decomposition block using moving average pool."""
        def __init__(self, kernel_size=3):
            super(SeriesDecomp, self).__init__()
            self.kernel_size = kernel_size
            self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=1, padding=0)

        def forward(self, x):
            # x shape: (Batch, Lookback, Features)
            # Transpose for AvgPool1d: (Batch, Features, Lookback)
            x_t = x.transpose(1, 2)
            pad_left = (self.kernel_size - 1) // 2
            pad_right = (self.kernel_size - 1) - pad_left
            front = x_t[:, :, 0:1].repeat(1, 1, pad_left)
            end = x_t[:, :, -1:].repeat(1, 1, pad_right)
            x_padded = torch.cat([front, x_t, end], dim=-1)
            trend_t = self.avg(x_padded)
            trend = trend_t.transpose(1, 2)
            seasonal = x - trend
            return seasonal, trend

    class GlacierDLinear(nn.Module):
        def __init__(self, lookback=5, input_dim=7, output_dim=1, kernel_size=3):
            super(GlacierDLinear, self).__init__()
            self.lookback = lookback
            self.input_dim = input_dim
            self.output_dim = output_dim

            self.decomposition = SeriesDecomp(kernel_size=kernel_size)
            
            # Linear projections mapping flattened (Lookback * Features) to Output
            self.linear_seasonal = nn.Linear(lookback * input_dim, output_dim)
            self.linear_trend = nn.Linear(lookback * input_dim, output_dim)

        def forward(self, x):
            # x shape: (Batch, Lookback, Features)
            seasonal, trend = self.decomposition(x)
            
            seasonal_flat = seasonal.reshape(x.shape[0], -1)
            trend_flat = trend.reshape(x.shape[0], -1)

            seasonal_out = self.linear_seasonal(seasonal_flat)
            trend_out = self.linear_trend(trend_flat)

            # Combined prediction: Trend + Seasonal
            out = seasonal_out + trend_out
            return out
else:
    class GlacierDLinear:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required to use GlacierDLinear.")

