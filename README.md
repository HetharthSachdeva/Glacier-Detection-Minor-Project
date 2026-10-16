# Multi-Season Glacier & Glacial Lake Semantic Segmentation
### A Comparative Study of Deep Learning Architectures on Multispectral Sentinel-2 Imagery

[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab%20%7C%20Linux%20%7C%20Windows-green.svg)]()
[![Data](https://img.shields.io/badge/Satellite-Copernicus%20Sentinel--2-blue.svg)]()

This repository provides an end-to-end deep learning framework for automated, high-precision glacier and glacial lake segmentation in rugged, high-mountain terrain (Ladakh Himalaya, Western Himalaya). It implements an **8-channel multispectral feature pipeline** and conducts a rigorous comparative study across three prominent semantic segmentation architectures:

1. **U-Net (Baseline)**: Classical symmetric convolutional contracting/expanding network.
2. **Attention U-Net**: U-Net augmented with **Attention Gates (AGs)** on skip connections to filter background terrain noise and isolate glacier boundaries.
3. **SUNet (Swin-UNet)**: Hybrid Vision Transformer network utilizing Shifted Window (Swin) Self-Attention blocks to model long-range spatial and spectral relationships.

---

## 📊 Benchmark Results

### 1. Real Sentinel-2 Multispectral Satellite Imagery + RGI 14 (Ladakh Himalaya)
Evaluated across **1,200 real $256 \times 256$ 8-channel patches** ($960$ train / $240$ val) paired with **Randolph Glacier Inventory (RGI 7.0/6.0 Region 14: South Asia West)** vector polygons covering over **4,800 real glaciers**:

| Rank | Model Architecture | Parameters ($\text{M}$) | Dice Score (F1) | IoU Score (Jaccard) | Precision | Recall | Key Insight |
|:---:|---|:---:|:---:|:---:|:---:|:---:|---|
| 🥇 | **Attention U-Net** | **31.39** | **0.9001** | **0.8183** | 0.9224 | **0.8788** | **Best Overall & Highest Boundary Recall** |
| 🥈 | **U-Net (Baseline)** | **31.04** | 0.8962 | 0.8119 | **0.9332** | 0.8620 | **Fast, Lightweight & High Precision** |
| 🥉 | **SUNet (Swin-UNet)** | 47.58 | 0.8806 | 0.7866 | 0.8930 | 0.8685 | Strong Global Context Capture |

> **Key Finding**: **Attention U-Net** surpassed the $0.90$ Dice milestone with the highest Recall ($87.88\%$), proving that Attention Gates on skip connections effectively suppress background rock and shadow noise, enabling better delineation of thin glacier margins and debris-covered ice.

---

### 2. High-Mountain Glacial Lake Benchmark (Kaggle 410 Dataset)
Evaluated on 410 high-resolution paired PNG images and masks (80% train / 20% val, 25 epochs):

| Model Architecture | Parameters ($\text{M}$) | Dice Score | IoU Score | Precision | Recall |
|---|:---:|:---:|:---:|:---:|:---:|
| **Attention U-Net** | **31.39** | **0.9668** | **0.9357** | 0.9527 | **0.9813** |
| **U-Net (Baseline)** | 31.04 | 0.9653 | 0.9329 | 0.9550 | 0.9758 |
| **SUNet (Swin-UNet)** | 47.58 | 0.9642 | 0.9308 | **0.9579** | 0.9705 |

---

## 🛰️ 8-Channel Input Data Specification

Instead of standard 3-channel RGB imagery, the primary framework processes an **8-channel multispectral tensor** of shape `(Batch, 8, 256, 256)`:

| Channel | Band / Index Name | Sentinel-2 Center Wavelength | Physical Purpose in Cryospheric Mapping |
|:---:|:---:|:---:|---|
| **1** | `B2` (Blue) | ~490 nm | Atmospheric scattering & water discrimination |
| **2** | `B3` (Green) | ~560 nm | Visible reflectance, core component of NDSI |
| **3** | `B4` (Red) | ~665 nm | Visible red absorption, core component of NDVI |
| **4** | `B8` (NIR) | ~842 nm | High reflectance for snow and ice |
| **5** | `B11` (SWIR-1) | ~1610 nm | Strong ice absorption (distinguishes snow/ice from clouds) |
| **6** | `B12` (SWIR-2) | ~2190 nm | Low reflectance for ice, high for moraines/rocks |
| **7** | `NDSI` | Formula below | Normalized Difference Snow Index |
| **8** | `NDVI` | Formula below | Normalized Difference Vegetation Index |

$$\text{NDSI} = \frac{\text{B3 (Green)} - \text{B11 (SWIR1)}}{\text{B3 (Green)} + \text{B11 (SWIR1)} + \epsilon}, \quad \text{NDVI} = \frac{\text{B8 (NIR)} - \text{B4 (Red)}}{\text{B8 (NIR)} + \text{B4 (Red)} + \epsilon}$$

*All channels are independently Min-Max normalized to the range $[0.0, 1.0]$.*

---

## 📁 Repository Structure

```
Minor_Project/
├── models/                                      # Model Architectures
│   ├── __init__.py                              # Exports UNet8Channel, AttentionUNet8Channel, SUNet8Channel
│   ├── unet.py                                  # Standard 8-Channel & 3-Channel U-Net
│   ├── attention_unet.py                        # U-Net with Skip Connection Attention Gates
│   └── sunet.py                                 # Swin-UNet (Spatial-Spectral Self-Attention)
│
├── dataset.py                                   # Dataset Loaders (Sentinel-2 8-ch .npy & PNG image pairs)
├── loss.py                                      # Hybrid BCE + Dice Loss (alpha = 0.5)
├── train.py                                     # Single model training script with checkpointing
├── evaluate.py                                  # Metric evaluation & optimal threshold sweep analysis
├── predict.py                                   # Full-scene sliding-window inference with Gaussian blending
├── compare.py                                   # Automated 3-model comparative benchmarking runner
├── create_test_data.py                          # Synthetic mock satellite patch generator for dry-runs
│
├── glacier_segmentation_comparative_study.ipynb # Interactive Google Colab GPU Notebook
├── README_COLAB.md                              # Step-by-step Colab GPU execution guide
│
├── comparative_metrics_real_sentinel2.csv       # Real Sentinel-2 benchmark metrics
├── sample_data_comparative_metrics.csv          # Sample dataset benchmark metrics
├── comparative_results/                         # Benchmark charts & overlay plots
│   ├── comparative_metrics_chart.png
│   └── comparative_predictions_overlay.png
│
├── environment.yml                              # Conda environment specification
├── requirements.txt                             # Pip dependencies specification
├── .gitignore                                   # Strict ignore rules for large datasets/weights
└── README.md                                    # Main project documentation
```

---

## ⚙️ Installation & Setup

### Option A: Using Conda (Recommended for Local Workstations)
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd Minor_Project

# Create and activate environment
conda env create -f environment.yml
conda activate glacier_unet
```

### Option B: Using Pip & Virtualenv
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1. Interactive Google Colab GPU Workflow (Recommended)
The fastest way to train on GPUs without local hardware constraints:
1. Upload [`glacier_segmentation_comparative_study.ipynb`](glacier_segmentation_comparative_study.ipynb) to [Google Colab](https://colab.research.google.com/).
2. Enable GPU acceleration: **Runtime -> Change runtime type -> Hardware accelerator -> GPU (T4)**.
3. Follow [`README_COLAB.md`](README_COLAB.md) to link your Google Drive folder containing the Sentinel-2 GeoTIFF tiles and RGI 14 shapefile.
4. Click **Runtime -> Run all**.

### 2. Run Comparative Benchmark Locally
To train and benchmark all 3 models under identical conditions:
```bash
# Running on unzipped image pairs (3-channel):
python compare.py --dataset-dir glacial-lake-dataset --in-channels 3 --epochs 25

# Running on Sentinel-2 8-channel patch directory:
python compare.py --dataset-dir data/real_patches --in-channels 8 --epochs 25
```

### 3. Train a Specific Model
```bash
python train.py --data-dir data/train --epochs 25 --batch-size 8 --lr 2e-4
```

### 4. Evaluate Threshold Sweep & Confusion Visualizations
```bash
python evaluate.py --checkpoint checkpoint/best_model.pth --data-dir data/val
```

### 5. Full-Scene Sliding-Window Inference
Applies Gaussian patch blending to stitch large satellite scenes without edge boundary artifacts:
```bash
python predict.py --input-scene data/scenes/sample_scene.npy --checkpoint checkpoint/best_model.pth --threshold 0.70
```

---

## 🛰️ Obtaining Real Data

1. **Sentinel-2 Multispectral Surface Reflectance (Level-2A)**:
   - Source: [Google Earth Engine](https://code.earthengine.google.com/) (`COPERNICUS/S2_SR_HARMONIZED`) or [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/).
   - Region: Ladakh Himalaya (`32.5°N - 35.5°N`, `75.5°E - 79.5°E`).
   - Seasonal Composites: Post-monsoon (September–October) provides minimal seasonal snow noise.

2. **Randolph Glacier Inventory (Ground-Truth Labels)**:
   - Source: [GLIMS Glacier Database](https://www.glims.org/RGI/) / [NSIDC RGI 7.0](https://nsidc.org/data/rgi/versions).
   - Region: **Region 14 (South Asia West)** covers Ladakh, Karakoram, and Western Himalaya.

---

## 🤝 Collaboration Guidelines

If you are contributing to this repository:
- **Do NOT commit dataset archives, raw GeoTIFFs, or `.pth` model checkpoints** to Git. These are strictly excluded via `.gitignore`.
- **Branching Policy**: Create a feature branch (`git checkout -b feature/model-improvement`) before submitting pull requests.
- **Model Interface**: When adding a new architecture in `models/`, ensure it accepts `in_channels` as a parameter (supporting both 3-channel and 8-channel inputs) and returns logits of shape `(Batch, 1, H, W)`.

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
