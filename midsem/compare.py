import os
import time
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm

from dataset import KaggleGlacialDataset, GlacierDataset
from loss import HybridBCEDiceLoss
from models import UNet8Channel as UNet, SUNet8Channel as SUNet, AttentionUNet8Channel as AttentionUNet

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad) / 1e6

def evaluate_metrics(model, dataloader, device, threshold=0.50):
    model.eval()
    tp, fp, fn, tn = 0, 0, 0, 0
    with torch.no_grad():
        for patches, masks in dataloader:
            patches, masks = patches.to(device), masks.to(device)
            probs = torch.sigmoid(model(patches))
            preds = (probs >= threshold).float()

            tp += (preds * masks).sum().item()
            fp += (preds * (1 - masks)).sum().item()
            fn += ((1 - preds) * masks).sum().item()
            tn += ((1 - preds) * (1 - masks)).sum().item()

    eps = 1e-8
    dice = (2.0 * tp) / (2.0 * tp + fp + fn + eps)
    iou = tp / (tp + fp + fn + eps)
    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)
    return dice, iou, precision, recall

def main():
    parser = argparse.ArgumentParser(description="Comparative Benchmark Study: UNet vs SUNet vs Attention UNet")
    parser.add_argument("--dataset-dir", type=str, default="glacial-lake-dataset", help="Path to unzipped Kaggle dataset folder")
    parser.add_argument("--in-channels", type=int, default=3, help="Number of input channels (3 for RGB PNG, 8 for Sentinel-2)")
    parser.add_argument("--epochs", type=int, default=25, help="Number of training epochs per model")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--output-dir", type=str, default="results", help="Directory to save comparative results")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running comparative study on device: {device}")

    # Dataset setup
    images_dir = os.path.join(args.dataset_dir, "images")
    masks_dir = os.path.join(args.dataset_dir, "masks")

    if not (os.path.exists(images_dir) and os.path.exists(masks_dir)):
        print(f"Error: Could not find '{images_dir}' or '{masks_dir}'. Make sure dataset is unzipped.")
        return

    img_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    full_ds = KaggleGlacialDataset(images_dir, masks_dir, img_files)

    train_size = int(0.8 * len(full_ds))
    val_size = len(full_ds) - train_size
    train_ds, val_ds = random_split(full_ds, [train_size, val_size], generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    # Models dictionary
    models = {
        "U-Net (Baseline)": UNet(in_channels=args.in_channels, out_channels=1),
        "Attention U-Net": AttentionUNet(in_channels=args.in_channels, out_channels=1),
        "SUNet (Swin-UNet)": SUNet(in_channels=args.in_channels, out_channels=1)
    }

    results = []
    trained_models = {}

    for name, model in models.items():
        print(f"\n=======================================================")
        print(f"   Training Model: {name} ({args.epochs} Epochs)")
        print(f"=======================================================")
        
        model = model.to(device)
        criterion = HybridBCEDiceLoss(alpha=0.5).to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)

        best_dice = 0.0
        best_metrics = (0, 0, 0, 0)

        for epoch in range(1, args.epochs + 1):
            model.train()
            train_loss = 0.0

            for bx, by in tqdm(train_loader, desc=f"{name} Epoch {epoch}/{args.epochs}", leave=False):
                bx, by = bx.to(device), by.to(device)
                optimizer.zero_grad()
                logits = model(bx)
                loss = criterion(logits, by)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            d, i, p, r = evaluate_metrics(model, val_loader, device, threshold=0.50)

            if d > best_dice:
                best_dice = d
                best_metrics = (d, i, p, r)
                torch.save(model.state_dict(), os.path.join(args.output_dir, f"{name.lower().replace(' ', '_')}_best.pth"))

            if epoch % 5 == 0 or epoch == args.epochs:
                print(f"   Epoch {epoch:02d}/{args.epochs} -> Dice: {d:.4f} | IoU: {i:.4f} | Precision: {p:.4f} | Recall: {r:.4f}")

        trained_models[name] = model
        params_m = count_parameters(model)

        results.append({
            "Model Architecture": name,
            "Parameters (M)": round(params_m, 2),
            "Dice Score": round(best_metrics[0], 4),
            "IoU Score": round(best_metrics[1], 4),
            "Precision": round(best_metrics[2], 4),
            "Recall": round(best_metrics[3], 4)
        })

    # Summary Table
    df = pd.DataFrame(results)
    print("\n=======================================================")
    print("         FINAL COMPARATIVE STUDY BENCHMARK          ")
    print("=======================================================")
    print(df.to_string(index=False))

    csv_path = os.path.join(args.output_dir, "comparative_metrics.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nSaved results table to '{csv_path}'")

    # Metrics Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df["Model Architecture"]))
    width = 0.2

    ax.bar(x - 1.5*width, df["Dice Score"], width, label="Dice Score", color='#1f77b4')
    ax.bar(x - 0.5*width, df["IoU Score"], width, label="IoU Score", color='#2ca02c')
    ax.bar(x + 0.5*width, df["Precision"], width, label="Precision", color='#ff7f0e')
    ax.bar(x + 1.5*width, df["Recall"], width, label="Recall", color='#d62728')

    ax.set_ylabel("Score")
    ax.set_title("Comparative Model Performance (410 Glacial Dataset)")
    ax.set_xticks(x)
    ax.set_xticklabels(df["Model Architecture"], fontweight="bold")
    ax.legend(loc="lower right")
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join(args.output_dir, "comparative_metrics_chart.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
