import torch
import torch.nn as nn
import torch.nn.functional as F

class DoubleConv(nn.Module):
    """
    (Conv3x3 -> BatchNorm -> ReLU) * 2
    """
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.conv(x)

class UNet8Channel(nn.Module):
    """
    Eight-Channel U-Net Architecture for Glacier Segmentation.
    Paper: "Multi-Season Glacier Mapping in the Ladakh Himalaya using Sentinel-2 Imagery 
            and an Eight-Channel U-Net Framework" (Sahu & Yasmin, 2026)
    Input shape: (B, 8, 256, 256) -> Output shape: (B, 1, 256, 256)
    """
    def __init__(self, in_channels=8, out_channels=1):
        super(UNet8Channel, self).__init__()
        
        # Encoder (Contracting Path)
        self.inc = DoubleConv(in_channels, 64)         # E1: 256x256x64
        self.down1 = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(64, 128)                        # E2: 128x128x128
        )
        self.down2 = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(128, 256)                       # E3: 64x64x256
        )
        self.down3 = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(256, 512)                       # E4: 32x32x512
        )
        self.down4 = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(512, 1024)                      # E5 (Bottleneck): 16x16x1024
        )

        # Decoder (Expanding Path)
        self.up1 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.conv_up1 = DoubleConv(1024, 512)          # D4: 32x32x512

        self.up2 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.conv_up2 = DoubleConv(512, 256)           # D3: 64x64x256

        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv_up3 = DoubleConv(256, 128)           # D2: 128x128x128

        self.up4 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv_up4 = DoubleConv(128, 64)            # D1: 256x256x64

        # Final 1x1 Convolution
        self.outc = nn.Conv2d(64, out_channels, kernel_size=1)

    def forward(self, x):
        # Encoder forward pass
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)

        # Decoder forward pass with Skip Connections
        x_up1 = self.up1(x5)
        x_concat1 = torch.cat([x_up1, x4], dim=1)
        x_d1 = self.conv_up1(x_concat1)

        x_up2 = self.up2(x_d1)
        x_concat2 = torch.cat([x_up2, x3], dim=1)
        x_d2 = self.conv_up2(x_concat2)

        x_up3 = self.up3(x_d2)
        x_concat3 = torch.cat([x_up3, x2], dim=1)
        x_d3 = self.conv_up3(x_concat3)

        x_up4 = self.up4(x_d3)
        x_concat4 = torch.cat([x_up4, x1], dim=1)
        x_d4 = self.conv_up4(x_concat4)

        logits = self.outc(x_d4)
        return logits

if __name__ == "__main__":
    # Test model shape consistency
    dummy_input = torch.randn(2, 8, 256, 256)
    model = UNet8Channel()
    output = model(dummy_input)
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output logits shape: {output.shape}")
    assert output.shape == (2, 1, 256, 256), "Output shape mismatch!"
    print("UNet8Channel architecture test passed!")
