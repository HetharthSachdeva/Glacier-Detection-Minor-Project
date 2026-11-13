import torch
import torch.nn as nn
import torch.nn.functional as F
from models.unet import DoubleConv

class SwinBlock(nn.Module):
    """
    Swin Transformer / Spatial-Spectral Attention Block for SUNet.
    Captures long-range spatial dependencies and multi-spectral band interactions.
    """
    def __init__(self, dim, num_heads=4):
        super(SwinBlock, self).__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(embed_dim=dim, num_heads=num_heads, batch_first=True)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Linear(dim * 4, dim)
        )

    def forward(self, x):
        # x shape: (B, C, H, W)
        B, C, H, W = x.shape
        x_flat = x.flatten(2).transpose(1, 2)  # (B, H*W, C)
        
        # Self-Attention
        x_norm = self.norm1(x_flat)
        attn_out, _ = self.attn(x_norm, x_norm, x_norm)
        x_flat = x_flat + attn_out
        
        # MLP Feed-forward
        x_flat = x_flat + self.mlp(self.norm2(x_flat))

        # Reshape back to image grid (B, C, H, W)
        out = x_flat.transpose(1, 2).view(B, C, H, W)
        return out

class SUNet8Channel(nn.Module):
    """
    Swin-UNet / SUNet 8-Channel Architecture for Glacier Segmentation.
    Combines Conv-encoder downsampling with Swin Transformer bottleneck and attention decoder.
    """
    def __init__(self, in_channels=8, out_channels=1):
        super(SUNet8Channel, self).__init__()
        
        # Encoder (Contracting Path)
        self.inc = DoubleConv(in_channels, 64)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(64, 128))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(128, 256))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(256, 512))
        
        # Swin Transformer Bottleneck
        self.down4 = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(512, 1024),
            SwinBlock(dim=1024, num_heads=8)
        )

        # Decoder (Expanding Path with Swin Transformer Blocks)
        self.up1 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.conv_up1 = nn.Sequential(DoubleConv(1024, 512), SwinBlock(dim=512, num_heads=4))

        self.up2 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.conv_up2 = nn.Sequential(DoubleConv(512, 256), SwinBlock(dim=256, num_heads=4))

        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv_up3 = DoubleConv(256, 128)

        self.up4 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv_up4 = DoubleConv(128, 64)

        # Final 1x1 Convolution
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

if __name__ == "__main__":
    dummy_input = torch.randn(2, 8, 256, 256)
    model = SUNet8Channel()
    output = model(dummy_input)
    print(f"SUNet 8-Channel forward test passed! Output shape: {output.shape}")
