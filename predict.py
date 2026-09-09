import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import torch

from dataset import compute_spectral_indices, normalize_channels
from model import UNet8Channel

def sliding_window_inference(model, scene_channels, patch_size=256, stride=128, threshold=0.70, device='cpu'):
    """
    Performs full-scene sliding window inference on large satellite composites.
    Paper Section 5.7:
    - Patch size: 256 x 256
    - Overlapping windows to reduce edge artifacts
    - Probability blending using weighted averaging
    """
    model.eval()
    C, H, W = scene_channels.shape
    
    prob_map = np.zeros((H, W), dtype=np.float32)
    weight_map = np.zeros((H, W), dtype=np.float32)

    # 2D Gaussian weight window for smooth patch blending
    y, x = np.ogrid[:patch_size, :patch_size]
    center = patch_size / 2.0
    sigma = patch_size / 4.0
    gaussian_weight = np.exp(-((x - center)**2 + (y - center)**2) / (2 * sigma**2))

    y_steps = list(range(0, H - patch_size + 1, stride))
    if (H - patch_size) % stride != 0:
        y_steps.append(H - patch_size)

    x_steps = list(range(0, W - patch_size + 1, stride))
    if (W - patch_size) % stride != 0:
        x_steps.append(W - patch_size)

    print(f"Running sliding window inference on scene shape ({H}, {W}) with stride={stride}...")

    with torch.no_grad():
        for y in y_steps:
            for x in x_steps:
                patch = scene_channels[:, y:y+patch_size, x:x+patch_size]
                
                # Check if channels need min-max norm
                patch_norm = normalize_channels(patch)
                patch_tensor = torch.from_numpy(patch_norm).float().unsqueeze(0).to(device)

                logits = model(patch_tensor)
                probs = torch.sigmoid(logits).squeeze().cpu().numpy()

                prob_map[y:y+patch_size, x:x+patch_size] += probs * gaussian_weight
                weight_map[y:y+patch_size, x:x+patch_size] += gaussian_weight

    # Normalize blended probability map
    weight_map[weight_map == 0] = 1.0
    final_prob_map = prob_map / weight_map
    binary_glacier_mask = (final_prob_map >= threshold).astype(np.uint8)

    return final_prob_map, binary_glacier_mask

def main():
    parser = argparse.ArgumentParser(description="Full-Scene Sliding-Window Glacier Inference")
    parser.add_argument("--input-scene", type=str, default="", help="Path to input .npy 6-band or 8-band full scene file")
    parser.add_argument("--checkpoint", type=str, default="checkpoint/best_model.pth", help="Path to trained model weights")
    parser.add_argument("--threshold", type=float, default=0.70, help="Glacier classification decision threshold (Paper default: 0.70)")
    parser.add_argument("--output-dir", type=str, default="predictions", help="Directory to save full-scene outputs")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load Model
    model = UNet8Channel(in_channels=8, out_channels=1).to(device)
    if os.path.exists(args.checkpoint):
        model.load_state_dict(torch.load(args.checkpoint, map_location=device))
        print(f"Loaded trained model weights from {args.checkpoint}")
    else:
        print(f"Warning: Checkpoint {args.checkpoint} not found. Running with initial weights.")

    # Generate or load full scene
    if args.input_scene and os.path.exists(args.input_scene):
        scene = np.load(args.input_scene)
    else:
        print("No input scene provided. Generating synthetic 512x512 full-scene satellite mosaic...")
        np.random.seed(100)
        H, W = 512, 512
        bands = np.random.uniform(0.05, 0.25, (6, H, W)).astype(np.float32)
        # Create glacier region in the center
        cy, cx, ry, rx = 256, 256, 120, 150
        y, x = np.ogrid[:H, :W]
        glacier_mask = ((y - cy)**2 / ry**2 + (x - cx)**2 / rx**2) <= 1.0
        
        bands[0][glacier_mask] += 0.5   # B2
        bands[1][glacier_mask] += 0.55  # B3
        bands[2][glacier_mask] += 0.5   # B4
        bands[3][glacier_mask] += 0.6   # B8
        bands[4][glacier_mask] += 0.05  # B11
        bands[5][glacier_mask] += 0.03  # B12

        scene = compute_spectral_indices(bands)

    if scene.shape[0] == 6:
        scene = compute_spectral_indices(scene)

    prob_map, binary_mask = sliding_window_inference(model, scene, patch_size=256, stride=128, threshold=args.threshold, device=device)

    # Plot & Save Full-Scene Prediction
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    rgb_preview = np.stack([scene[3], scene[2], scene[1]], axis=-1)
    rgb_preview = (rgb_preview - rgb_preview.min()) / (rgb_preview.max() - rgb_preview.min() + 1e-8)

    axes[0].imshow(rgb_preview)
    axes[0].set_title("Sentinel-2 Scene Composite (RGB)")
    axes[0].axis('off')

    axes[1].imshow(prob_map, cmap='Blues')
    axes[1].set_title("Full-Scene Probability Map")
    axes[1].axis('off')

    axes[2].imshow(binary_mask, cmap='bone')
    axes[2].set_title(f"Binary Glacier Segmentation Mask\n(Threshold = {args.threshold:.2f})")
    axes[2].axis('off')

    plt.tight_layout()
    out_img_path = os.path.join(args.output_dir, "full_scene_prediction.png")
    plt.savefig(out_img_path, dpi=300)
    plt.close()

    np.save(os.path.join(args.output_dir, "full_scene_glacier_mask.npy"), binary_mask)
    print(f"Saved full-scene prediction visualization to {out_img_path}")
    print(f"Saved binary glacier mask array to {os.path.join(args.output_dir, 'full_scene_glacier_mask.npy')}")

if __name__ == "__main__":
    main()
