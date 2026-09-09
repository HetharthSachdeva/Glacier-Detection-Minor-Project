import torch
import torch.nn as nn
import torch.nn.functional as F

class DoubleConv(nn.Module):
    """(Conv3x3 -> BatchNorm -> ReLU) * 2"""
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
    Standard 8-Channel U-Net Architecture.
    Paper: "Multi-Season Glacier Mapping in the Ladakh Himalaya using Sentinel-2 Imagery 
            and an Eight-Channel U-Net Framework" (Sahu & Yasmin, 2026)
    """
    def __init__(self, in_channels=8, out_channels=1):
        super(UNet8Channel, self).__init__()
        
        # Encoder (Contracting Path)
        self.inc = DoubleConv(in_channels, 64)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(64, 128))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(128, 256))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(256, 512))
        self.down4 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(512, 1024))

        # Decoder (Expanding Path)
        self.up1 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.conv_up1 = DoubleConv(1024, 512)

        self.up2 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.conv_up2 = DoubleConv(512, 256)

        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv_up3 = DoubleConv(256, 128)

        self.up4 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv_up4 = DoubleConv(128, 64)

        # Output Convolution
        self.outc = nn.Conv2d(64, out_channels, kernel_size=1)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)

        x_up1 = self.up1(x5)
        x_d1 = self.conv_up1(torch.cat([x_up1, x4], dim=1))

        x_up2 = self.up2(x_d1)
        x_d2 = self.conv_up2(torch.cat([x_up2, x3], dim=1))

        x_up3 = self.up3(x_d2)
        x_d3 = self.conv_up3(torch.cat([x_up3, x2], dim=1))

        x_up4 = self.up4(x_d3)
        x_d4 = self.conv_up4(torch.cat([x_up4, x1], dim=1))

        logits = self.outc(x_d4)
        return logits
