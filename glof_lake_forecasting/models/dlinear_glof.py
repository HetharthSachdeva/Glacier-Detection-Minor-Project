"""
Model 4: DLinear (Trend-Seasonal Decomposition) for GLOF Prediction
--------------------------------------------------------------------
Based on Zeng et al. (AAAI 2023). Decomposes lake sequence into steady multi-year 
expansion trend and seasonal meltwater inflow fluctuations.
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
        def __init__(self, kernel_size=3):
            super().__init__()
            self.kernel_size = kernel_size
            self.avg = nn.AvgPool1d(kernel_size=kernel_size, stride=1, padding=0)

        def forward(self, x):
            x_t = x.transpose(1, 2)
            pl = (self.kernel_size - 1) // 2
            pr = (self.kernel_size - 1) - pl
            front = x_t[:, :, 0:1].repeat(1, 1, pl)
            end = x_t[:, :, -1:].repeat(1, 1, pr)
            x_pad = torch.cat([front, x_t, end], dim=-1)
            trend = self.avg(x_pad).transpose(1, 2)
            seasonal = x - trend
            return seasonal, trend

    class GLOFDLinear(nn.Module):
        def __init__(self, lookback=6, input_dim=7, num_classes=3, kernel_size=3):
            super().__init__()
            self.decomp = SeriesDecomp(kernel_size=kernel_size)
            in_flat = lookback * input_dim
            # Linear heads for Trend & Seasonal components
            self.l_trend = nn.Linear(in_flat, 1)
            self.l_seasonal = nn.Linear(in_flat, 1)
            # Classification head for GLOF hazard risk
            self.risk_head = nn.Linear(in_flat, num_classes)

        def forward(self, x):
            seasonal, trend = self.decomp(x)
            s_flat = seasonal.reshape(x.shape[0], -1)
            t_flat = trend.reshape(x.shape[0], -1)
            pred_area = self.l_seasonal(s_flat) + self.l_trend(t_flat)
            risk_logits = self.risk_head(t_flat)
            return pred_area, risk_logits
else:
    class GLOFDLinear:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for GLOFDLinear.")

