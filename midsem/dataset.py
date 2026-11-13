import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as T

def compute_spectral_indices(bands):
    """
    Computes NDSI and NDVI from 6 Sentinel-2 spectral bands.
    bands shape: (6, H, W)
      0: B2 (Blue), 1: B3 (Green), 2: B4 (Red), 3: B8 (NIR), 4: B11 (SWIR1), 5: B12 (SWIR2)
    Returns 8-channel array of shape (8, H, W).
    """
    b3_green = bands[1].astype(np.float32)
    b4_red = bands[2].astype(np.float32)
    b8_nir = bands[3].astype(np.float32)
    b11_swir1 = bands[4].astype(np.float32)

    eps = 1e-8
    ndsi = (b3_green - b11_swir1) / (b3_green + b11_swir1 + eps)
    ndvi = (b8_nir - b4_red) / (b8_nir + b4_red + eps)

    ndsi_norm = (ndsi + 1.0) / 2.0
    ndvi_norm = (ndvi + 1.0) / 2.0

    return np.concatenate([bands.astype(np.float32), 
                              ndsi_norm[np.newaxis, ...], 
                              ndvi_norm[np.newaxis, ...]], axis=0)

def normalize_channels(channels):
    """Min-Max normalizes channels independently to [0, 1]."""
    norm_channels = np.zeros_like(channels, dtype=np.float32)
    for c in range(channels.shape[0]):
        c_min = channels[c].min()
        c_max = channels[c].max()
        if c_max - c_min > 1e-8:
            norm_channels[c] = (channels[c] - c_min) / (c_max - c_min)
        else:
            norm_channels[c] = channels[c]
    return norm_channels

class KaggleGlacialDataset(Dataset):
    """
    PyTorch Dataset loader for Kaggle 410 Glacial Dataset PNG image/mask pairs.
    """
    def __init__(self, images_dir, masks_dir, img_files=None, image_size=(256, 256)):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        if img_files is not None:
            self.img_files = img_files
        else:
            self.img_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])

        self.img_transform = T.Compose([
            T.Resize(image_size),
            T.ToTensor()
        ])
        self.mask_transform = T.Compose([
            T.Resize(image_size),
            T.ToTensor()
        ])

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):
        fname = self.img_files[idx]
        img_path = os.path.join(self.images_dir, fname)
        mask_path = os.path.join(self.masks_dir, fname)

        img = Image.open(img_path).convert('RGB')
        mask = Image.open(mask_path).convert('L')

        img_tensor = self.img_transform(img)
        mask_tensor = (self.mask_transform(mask) > 0.5).float()
        return img_tensor, mask_tensor

class GlacierDataset(Dataset):
    """
    General Dataset loader for Sentinel-2 8-channel .npy arrays or PNG image pairs.
    """
    def __init__(self, data_dir=None, patches=None, masks=None):
        if data_dir is not None and os.path.exists(data_dir):
            # Check for PNG pairs or NPY patches
            if os.path.exists(os.path.join(data_dir, "images")):
                self.dataset = KaggleGlacialDataset(os.path.join(data_dir, "images"), os.path.join(data_dir, "masks"))
                self.is_png = True
            else:
                self.patch_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('_patch.npy')]
                self.mask_files = [f.replace('_patch.npy', '_mask.npy') for f in self.patch_files]
                self.is_png = False
        else:
            raise ValueError("Data directory does not exist.")

    def __len__(self):
        return len(self.dataset) if self.is_png else len(self.patch_files)

    def __getitem__(self, idx):
        if self.is_png:
            return self.dataset[idx]
        else:
            patch = np.load(self.patch_files[idx])
            mask = np.load(self.mask_files[idx])
            if patch.shape[0] == 6:
                patch = compute_spectral_indices(patch)
            patch = normalize_channels(patch)
            return torch.from_numpy(patch).float(), torch.from_numpy(mask).float().unsqueeze(0)
