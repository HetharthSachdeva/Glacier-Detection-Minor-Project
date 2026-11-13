import os
import numpy as np
from dataset import compute_spectral_indices

def create_test_dataset(output_dir="test_data", num_patches=10, scene_shape=(512, 512)):
    """
    Creates a dedicated test_data directory containing:
    1. test_data/patches: 8-channel Sentinel-2 test patches (256x256) and binary glacier masks
    2. test_data/scenes: Full multispectral satellite scenes (512x512) for sliding window testing
    """
    patches_dir = os.path.join(output_dir, "patches")
    scenes_dir = os.path.join(output_dir, "scenes")
    
    os.makedirs(patches_dir, exist_ok=True)
    os.makedirs(scenes_dir, exist_ok=True)

    np.random.seed(2026)
    print(f"Creating test dataset in '{output_dir}/'...")

    # 1. Generate 256x256 test patches
    H, W = 256, 256
    for i in range(num_patches):
        mask = np.zeros((H, W), dtype=np.float32)
        # Create 1-2 random circular glacier regions
        cy, cx = np.random.randint(60, H-60), np.random.randint(60, W-60)
        ry, rx = np.random.randint(30, 70), np.random.randint(30, 70)
        y, x = np.ogrid[:H, :W]
        glacier_region = ((y - cy)**2 / ry**2 + (x - cx)**2 / rx**2) <= 1.0
        mask[glacier_region] = 1.0

        # Simulate 6 Sentinel-2 bands
        bands = np.zeros((6, H, W), dtype=np.float32)
        for b in range(6):
            bands[b] = np.random.uniform(0.08, 0.20, (H, W))

        glacier_idx = (mask == 1.0)
        bands[0][glacier_idx] += np.random.uniform(0.45, 0.65, np.sum(glacier_idx)) # Blue (B2)
        bands[1][glacier_idx] += np.random.uniform(0.50, 0.70, np.sum(glacier_idx)) # Green (B3)
        bands[2][glacier_idx] += np.random.uniform(0.45, 0.65, np.sum(glacier_idx)) # Red (B4)
        bands[3][glacier_idx] += np.random.uniform(0.55, 0.75, np.sum(glacier_idx)) # NIR (B8)
        bands[4][glacier_idx] += np.random.uniform(0.03, 0.12, np.sum(glacier_idx)) # SWIR1 (B11)
        bands[5][glacier_idx] += np.random.uniform(0.02, 0.10, np.sum(glacier_idx)) # SWIR2 (B12)

        non_glacier = ~glacier_idx
        bands[4][non_glacier] += np.random.uniform(0.22, 0.45, np.sum(non_glacier))
        bands[5][non_glacier] += np.random.uniform(0.20, 0.40, np.sum(non_glacier))

        # Compute 8-channel array
        eight_channel_patch = compute_spectral_indices(bands)

        np.save(os.path.join(patches_dir, f"test_patch_{i:02d}_patch.npy"), eight_channel_patch)
        np.save(os.path.join(patches_dir, f"test_patch_{i:02d}_mask.npy"), mask)

    print(f"Generated {num_patches} test patches in '{patches_dir}/'")

    # 2. Generate full-scene 512x512 satellite test scenes
    sH, sW = scene_shape
    for s in range(2):
        scene_bands = np.zeros((6, sH, sW), dtype=np.float32)
        for b in range(6):
            scene_bands[b] = np.random.uniform(0.05, 0.22, (sH, sW))

        # Create multiple glacier systems across the scene
        g_mask = np.zeros((sH, sW), dtype=bool)
        for _ in range(3):
            cy, cx = np.random.randint(100, sH-100), np.random.randint(100, sW-100)
            ry, rx = np.random.randint(50, 110), np.random.randint(50, 110)
            sy, sx = np.ogrid[:sH, :sW]
            g_mask |= (((sy - cy)**2 / ry**2 + (sx - cx)**2 / rx**2) <= 1.0)

        scene_bands[0][g_mask] += 0.50
        scene_bands[1][g_mask] += 0.55
        scene_bands[2][g_mask] += 0.50
        scene_bands[3][g_mask] += 0.60
        scene_bands[4][g_mask] += 0.05
        scene_bands[5][g_mask] += 0.03

        scene_8ch = compute_spectral_indices(scene_bands)
        np.save(os.path.join(scenes_dir, f"test_scene_{s:02d}.npy"), scene_8ch)

    print(f"Generated 2 test satellite full scenes in '{scenes_dir}/'")
    print(f"Test data setup complete!")

if __name__ == "__main__":
    create_test_dataset()
