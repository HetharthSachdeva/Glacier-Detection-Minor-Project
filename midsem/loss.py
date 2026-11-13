import torch
import torch.nn as nn
import torch.nn.functional as F

class DiceLoss(nn.Module):
    """
    Soft Dice Loss for binary segmentation.
    Dice = 2 * |P ∩ G| / (|P| + |G| + eps)
    DiceLoss = 1 - Dice
    """
    def __init__(self, smooth=1e-6):
        super(DiceLoss, self).__init__()
        self.smooth = smooth

    def forward(self, logits, targets):
        probs = torch.sigmoid(logits)
        
        # Flatten predictions and targets
        probs_flat = probs.view(-1)
        targets_flat = targets.view(-1)
        
        intersection = (probs_flat * targets_flat).sum()
        total_area = probs_flat.sum() + targets_flat.sum()
        
        dice = (2.0 * intersection + self.smooth) / (total_area + self.smooth)
        return 1.0 - dice

class HybridBCEDiceLoss(nn.Module):
    """
    Hybrid Loss function combining Binary Cross Entropy (BCE) and Dice Loss.
    Equation (2) from Paper:
    Loss = alpha * BCE + (1 - alpha) * DiceLoss
    Default alpha = 0.5 as specified in Section 5.3 of the paper.
    """
    def __init__(self, alpha=0.5, pos_weight=None):
        super(HybridBCEDiceLoss, self).__init__()
        self.alpha = alpha
        self.bce_loss = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        self.dice_loss = DiceLoss()

    def forward(self, logits, targets):
        bce = self.bce_loss(logits, targets)
        dice = self.dice_loss(logits, targets)
        return self.alpha * bce + (1.0 - self.alpha) * dice

if __name__ == "__main__":
    dummy_logits = torch.randn(4, 1, 256, 256)
    dummy_targets = torch.randint(0, 2, (4, 1, 256, 256)).float()
    
    criterion = HybridBCEDiceLoss(alpha=0.5)
    loss = criterion(dummy_logits, dummy_targets)
    print(f"Hybrid BCE + Dice Loss value: {loss.item():.4f}")
