import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from dataset import GlacierDataset
from model import UNet8Channel

def compute_confusion_metrics(preds, targets):
    """
    Computes TP, FP, FN, TN for binary tensors.
    """
    tp = (preds * targets).sum().item()
    fp = (preds * (1 - targets)).sum().item()
    fn = ((1 - preds) * targets).sum().item()
    tn = ((1 - preds) * (1 - targets)).sum().item()
    return tp, fp, fn, tn

def evaluate_threshold(model, dataloader, threshold, device):
    model.eval()
    total_tp, total_fp, total_fn, total_tn = 0, 0, 0, 0

    with torch.no_grad():
        for patches, masks in dataloader:
            patches, masks = patches.to(device), masks.to(device)
            logits = model(patches)
            probs = torch.sigmoid(logits)
            preds = (probs >= threshold).float()

            tp, fp, fn, tn = compute_confusion_metrics(preds, masks)
            total_tp += tp
            total_fp += fp
            total_fn += fn
            total_tn += tn

    eps = 1e-8
    dice = (2.0 * total_tp) / (2.0 * total_tp + total_fp + total_fn + eps)
    iou = total_tp / (total_tp + total_fp + total_fn + eps)
    precision = total_tp / (total_tp + total_fp + eps)
    recall = total_tp / (total_tp + total_fn + eps)

    return {"dice": dice, "iou": iou, "precision": precision, "recall": recall, 
            "tp": total_tp, "fp": total_fp, "fn": total_fn, "tn": total_tn}

def generate_confusion_map(pred, target):
    """
    Generates color-coded evaluation visualization map:
    - Green (0, 255, 0): True Positive (TP)
    - Red (255, 0, 0): False Positive (FP)
    - Yellow (255, 255, 0): False Negative (FN)
    - Black (0, 0, 0): True Negative (TN)
    """
    H, W = pred.shape
    vis_map = np.zeros((H, W, 3), dtype=np.uint8)

    tp_mask = (pred == 1) & (target == 1)
    fp_mask = (pred == 1) & (target == 0)
    fn_mask = (pred == 0) & (target == 1)

    vis_map[tp_mask] = [0, 220, 0]     # Green for TP
    vis_map[fp_mask] = [220, 0, 0]     # Red for FP
    vis_map[fn_mask] = [220, 220, 0]   # Yellow for FN

    return vis_map

def main():
    parser = argparse.ArgumentParser(description="Evaluate 8-Channel U-Net Glacier Segmentation Framework")
    parser.add_argument("--data-dir", type=str, default="data/synthetic/val", help="Path to evaluation dataset")
    parser.add_argument("--checkpoint", type=str, default="checkpoint/best_model.pth", help="Path to model weights")
    parser.add_argument("--output-dir", type=str, default="evaluation_results", help="Output directory for plots")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load Dataset and Model
    val_dataset = GlacierDataset(data_dir=args.data_dir)
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

    model = UNet8Channel(in_channels=8, out_channels=1).to(device)
    if os.path.exists(args.checkpoint):
        model.load_state_dict(torch.load(args.checkpoint, map_location=device))
        print(f"Loaded model weights from {args.checkpoint}")
    else:
        print(f"Warning: Checkpoint {args.checkpoint} not found. Running with randomly initialized weights.")

    # 1. Threshold Sweep Analysis (Section 5.6 / 6.2)
    thresholds = np.arange(0.10, 0.95, 0.05)
    sweep_results = []
    print("\n--- Performing Threshold Sweep Analysis ---")
    print(f"{'Threshold':<10} | {'Dice':<8} | {'IoU':<8} | {'Precision':<10} | {'Recall':<8}")
    print("-" * 55)

    best_thresh = 0.70
    best_dice = 0.0
    best_metrics = None

    for th in thresholds:
        res = evaluate_threshold(model, val_loader, th, device)
        sweep_results.append(res)
        print(f"{th:<10.2f} | {res['dice']:<8.4f} | {res['iou']:<8.4f} | {res['precision']:<10.4f} | {res['recall']:<8.4f}")
        
        if res['dice'] > best_dice:
            best_dice = res['dice']
            best_thresh = th
            best_metrics = res

    print("-" * 55)
    print(f"Optimal Threshold identified: {best_thresh:.2f} (Dice: {best_metrics['dice']:.4f}, IoU: {best_metrics['iou']:.4f})")

    # 2. Plot Performance Metrics (Figure 6 in paper)
    metrics_names = ['Dice', 'IoU', 'Precision', 'Recall']
    metrics_values = [best_metrics['dice'], best_metrics['iou'], best_metrics['precision'], best_metrics['recall']]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics_names, metrics_values, color=['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728'], width=0.5)
    plt.ylim(0, 1.05)
    plt.ylabel('Score')
    plt.title(f'Glacier Segmentation Performance Metrics (Threshold = {best_thresh:.2f})')

    for bar, val in zip(bars, metrics_values):
        plt.text(bar.get_x() + bar.get_width()/2.0, val + 0.02, f'{val:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plot_path = os.path.join(args.output_dir, "performance_metrics.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved performance metrics bar chart to {plot_path}")

    # 3. Generate Confusion Map Sample Visualization (Figure 7 in paper)
    model.eval()
    sample_patch, sample_mask = val_dataset[0]
    sample_patch_batch = sample_patch.unsqueeze(0).to(device)
    
    with torch.no_grad():
        logits = model(sample_patch_batch)
        probs = torch.sigmoid(logits).squeeze().cpu().numpy()
        preds = (probs >= best_thresh).astype(np.uint8)
        target = sample_mask.squeeze().cpu().numpy().astype(np.uint8)

    confusion_vis = generate_confusion_map(preds, target)

    # Plot sample prediction vs evaluation map
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # False color composite (B8, B4, B3) for RGB preview
    patch_np = sample_patch.numpy()
    rgb_preview = np.stack([patch_np[3], patch_np[2], patch_np[1]], axis=-1)
    rgb_preview = (rgb_preview - rgb_preview.min()) / (rgb_preview.max() - rgb_preview.min() + 1e-8)

    axes[0].imshow(rgb_preview)
    axes[0].set_title("Input False Color Composite")
    axes[0].axis('off')

    axes[1].imshow(probs, cmap='Blues')
    axes[1].set_title("Predicted Glacier Probability Map")
    axes[1].axis('off')

    axes[2].imshow(confusion_vis)
    axes[2].set_title("Segmentation Evaluation Map\n(Green: TP, Red: FP, Yellow: FN, Black: TN)")
    axes[2].axis('off')

    plt.tight_layout()
    vis_path = os.path.join(args.output_dir, "evaluation_map_visualization.png")
    plt.savefig(vis_path, dpi=300)
    plt.close()
    print(f"Saved evaluation map visualization to {vis_path}")

if __name__ == "__main__":
    main()
