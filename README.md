# Deep Learning-Based Glacier & Glacial Lake Semantic Segmentation: A Comparative Study

This repository presents a comparative research study evaluating **three state-of-the-art semantic segmentation architectures** for automated glacier and glacial lake mapping:

1. **U-Net (Baseline)**: Standard convolutional encoder-decoder network with skip connections.
2. **SUNet (Swin-UNet)**: Hybrid Vision Transformer network utilizing Shifted Window Self-Attention blocks to model global spatial and spectral relationships.
3. **Attention U-Net**: U-Net integrated with **Attention Gates (AGs)** on skip connections to automatically suppress non-target background terrain noise (rocks, shadows) while isolating glacier boundaries.

---

## 📊 Benchmark Results Obtained (25 Epochs on GPU)

Evaluating the three architectures under identical training conditions on the **410 Glacial Dataset** yielded the following comparative performance:

| Rank | Model Architecture | Parameters ($\text{M}$) | Dice Score (F1) | IoU Score (Jaccard) | Precision | Recall | Highlight |
|---|---|---|---|---|---|---|---|
| 🥇 **1st** | **Attention U-Net** | **31.39** | **0.9668** | **0.9357** | 0.9527 | **0.9813** | **Best Overall & Highest Recall** |
| 🥈 **2nd** | **U-Net (Baseline)** | **31.04** | 0.9653 | 0.9329 | 0.9550 | 0.9758 | **Fast & Lightweight Baseline** |
| 🥉 **3rd** | **SUNet (Swin-UNet)** | 47.58 | 0.9642 | 0.9308 | **0.9579** | 0.9705 | **Highest Precision (Lowest False Positives)** |

---

## 📁 Current Dataset Used

Currently, the project uses the **Kaggle 410 Glacial Dataset** (`glacial-lake-dataset` / `archive.zip`):
- **410 Paired PNG Images & Binary Masks**: High-resolution imagery of high-mountain glacial systems and glacial lakes.
- **Data Division**: **80% Training** (328 pairs) and **20% Validation** (82 pairs).
- **Target Encoding**: Binary mask ($1.0 =$ Glacier / Lake, $0.0 =$ Background terrain).

---

## 🛰️ Where to Obtain Real Multispectral Sentinel-2 Satellite Data

To transition from 3-channel RGB PNG imagery to full **8-channel multispectral Sentinel-2 satellite data**:

### 1. Google Earth Engine (GEE)
- **Asset ID**: `COPERNICUS/S2_SR_HARMONIZED` (Sentinel-2 Level-2A Surface Reflectance).
- **Bands**: `B2` (Blue), `B3` (Green), `B4` (Red), `B8` (NIR), `B11` (SWIR1), `B12` (SWIR2) at 10m spatial resolution.
- **Spectral Indices Computed**:
  $$\text{NDSI} = \frac{\text{B3} - \text{B11}}{\text{B3} + \text{B11} + \epsilon}, \quad \text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4} + \epsilon}$$
- **Access**: Free online at [code.earthengine.google.com](https://code.earthengine.google.com/).

### 2. Copernicus Data Space Ecosystem
- **URL**: [dataspace.copernicus.eu](https://dataspace.copernicus.eu/)
- Direct download of Sentinel-2 L2A `.SAFE` scene archives and GeoTIFFs.

### 3. Randolph Glacier Inventory (RGI 6.0 / RGI 7.0 Ground Truth)
- **URL**: [GLIMS Glacier Database](https://www.glims.org/RGI/) or [NSIDC](https://nsidc.org/data/rgi/versions)
- Vector polygon shapefiles (`.shp`) of glacier boundaries digitized by glaciologists worldwide.

---

## 🔄 How to Switch Datasets & Run Models

The codebase is designed to seamlessly switch between **3-channel PNG data** and **8-channel Sentinel-2 array data**:

### 1. Running on 3-Channel RGB PNG Data (Default)
In your code or Colab notebook:
```python
model = AttentionUNet(in_channels=3, out_channels=1)
```

### 2. Running on 8-Channel Sentinel-2 Multispectral Data
Pass `in_channels=8` when instantiating the models:
```python
model = AttentionUNet(in_channels=8, out_channels=1)
```

---

## 🚀 Execution Guide

### Option A: Google Colab GPU (Recommended)
1. Open Google Colab and upload [`glacier_segmentation_comparative_study.ipynb`](file:///d:/Coding/Minor_Project/glacier_segmentation_comparative_study.ipynb).
2. Upload `archive.zip` to Colab's file sidebar.
3. Enable GPU (**Runtime -> Change runtime type -> Hardware accelerator -> GPU**).
4. Click **Runtime -> Run all**.

### Option B: Local Training
```bash
conda activate glacier_unet
python compare.py --dataset-dir glacial-lake-dataset --in-channels 3 --epochs 25
```

---

## 🗂️ Project Directory Structure

```
Minor_Project/
├── models/
│   ├── unet.py                             # 8-channel & 3-channel U-Net
│   ├── sunet.py                            # SUNet (Swin-UNet)
│   └── attention_unet.py                  # Attention U-Net
├── dataset.py                              # Dataset loaders (Kaggle PNG & Sentinel-2 .npy)
├── loss.py                                 # Hybrid BCE + Dice Loss
├── compare.py                              # Comparative benchmark script
├── glacier_segmentation_comparative_study.ipynb  # Interactive Google Colab GPU Notebook
├── environment.yml                         # Conda environment definition file
├── comparative_metrics.csv                 # Exported benchmark performance results
└── README.md                               # Project documentation
```
