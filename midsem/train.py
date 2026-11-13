import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from dataset import GlacierDataset, generate_synthetic_glacier_dataset
from model import UNet8Channel
from loss import HybridBCEDiceLoss

def calculate_dice(logits, targets, threshold=0.5):
    probs = torch.sigmoid(logits)
    preds = (probs >= threshold).float()
    preds_flat = preds.view(-1)
    targets_flat = targets.view(-1)
    
    intersection = (preds_flat * targets_flat).sum()
    total = preds_flat.sum() + targets_flat.sum()
    if total == 0:
        return 1.0
    return (2.0 * intersection / total).item()

def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    running_dice = 0.0

    for patches, masks in tqdm(dataloader, desc="Training", leave=False):
        patches, masks = patches.to(device), masks.to(device)
        
        optimizer.zero_grad()
        logits = model(patches)
        loss = criterion(logits, masks)
        loss.backward()

        # Gradient clipping to prevent exploding gradients (Section 5.4)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        running_loss += loss.item() * patches.size(0)
        running_dice += calculate_dice(logits, masks) * patches.size(0)

    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_dice = running_dice / len(dataloader.dataset)
    return epoch_loss, epoch_dice

def validate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_dice = 0.0

    with torch.no_grad():
        for patches, masks in tqdm(dataloader, desc="Validation", leave=False):
            patches, masks = patches.to(device), masks.to(device)
            logits = model(patches)
            loss = criterion(logits, masks)

            running_loss += loss.item() * patches.size(0)
            running_dice += calculate_dice(logits, masks) * patches.size(0)

    val_loss = running_loss / len(dataloader.dataset)
    val_dice = running_dice / len(dataloader.dataset)
    return val_loss, val_dice

def main():
    parser = argparse.ArgumentParser(description="Train 8-Channel U-Net Glacier Segmentation Framework")
    parser.add_argument("--data-dir", type=str, default="data/synthetic", help="Path to dataset directory")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size (Paper default: 8)")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate for AdamW (Paper default: 2e-4)")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="Weight decay for regularization")
    parser.add_argument("--output-dir", type=str, default="checkpoint", help="Directory to save model weights & logs")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Check or generate synthetic dataset
    train_dir = os.path.join(args.data_dir, "train")
    val_dir = os.path.join(args.data_dir, "val")
    if not (os.path.exists(train_dir) and len(os.listdir(train_dir)) > 0):
        print("Data directory empty or missing. Generating synthetic Sentinel-2 glacier dataset...")
        generate_synthetic_glacier_dataset(output_dir=args.data_dir, num_samples=100)

    # Datasets and DataLoaders
    train_dataset = GlacierDataset(data_dir=train_dir)
    val_dataset = GlacierDataset(data_dir=val_dir)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    # Model, Loss, Optimizer
    model = UNet8Channel(in_channels=8, out_channels=1).to(device)
    criterion = HybridBCEDiceLoss(alpha=0.5).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    best_val_dice = 0.0
    history = {"train_loss": [], "train_dice": [], "val_loss": [], "val_dice": []}

    print(f"\nStarting training for {args.epochs} epochs...")
    print(f"{'Epoch':<6} | {'Train Loss':<10} | {'Train Dice':<10} | {'Val Loss':<10} | {'Val Dice':<10}")
    print("-" * 55)

    for epoch in range(1, args.epochs + 1):
        t_loss, t_dice = train_epoch(model, train_loader, criterion, optimizer, device)
        v_loss, v_dice = validate(model, val_loader, criterion, device)

        history["train_loss"].append(t_loss)
        history["train_dice"].append(t_dice)
        history["val_loss"].append(v_loss)
        history["val_dice"].append(v_dice)

        print(f"{epoch:<6} | {t_loss:<10.4f} | {t_dice:<10.4f} | {v_loss:<10.4f} | {v_dice:<10.4f}")

        # Save best checkpoint
        if v_dice > best_val_dice:
            best_val_dice = v_dice
            model_path = os.path.join(args.output_dir, "best_model.pth")
            torch.save(model.state_dict(), model_path)

    print(f"\nTraining completed! Best Validation Dice Score: {best_val_dice:.4f}")
    print(f"Saved best model checkpoint to {os.path.join(args.output_dir, 'best_model.pth')}")

    # Plot & Save Training History
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, args.epochs + 1), history["train_loss"], label="Train Loss")
    plt.plot(range(1, args.epochs + 1), history["val_loss"], label="Val Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Hybrid BCE + Dice Loss")
    plt.title("Training & Validation Loss")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(range(1, args.epochs + 1), history["train_dice"], label="Train Dice")
    plt.plot(range(1, args.epochs + 1), history["val_dice"], label="Val Dice")
    plt.xlabel("Epoch")
    plt.ylabel("Dice Score")
    plt.title("Training & Validation Dice Score")
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(args.output_dir, "training_history.png")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved training history plot to {plot_path}")

if __name__ == "__main__":
    main()
