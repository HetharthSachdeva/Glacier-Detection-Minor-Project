# Google Colab GPU Guide - Real Sentinel-2 & RGI 14 Comparative Study

This guide explains how to run the comparative study on **Real Sentinel-2 8-Channel Imagery** and **Randolph Glacier Inventory (RGI 14)** directly in Google Colab using your Google Drive files.

---

## 📁 Google Drive Setup

Make sure your Google Drive folder named **`Minor_Project`** has:
1. The **12 Sentinel-2 GeoTIFF files** (`*.tif`) exported from Google Earth Engine.
2. The zip file: **`RGI2000-v7.0-G-14_south_asia_west.zip`**.

Path in Google Drive: `My Drive / Minor_Project /`

---

## 🚀 How to Run on Google Colab

### Step 1: Open Google Colab & Upload Notebook
1. Open [colab.research.google.com](https://colab.research.google.com/).
2. Click **Upload** -> Select [`glacier_segmentation_comparative_study.ipynb`](file:///d:/Coding/Minor_Project/glacier_segmentation_comparative_study.ipynb).

### Step 2: Enable GPU
1. Click **Runtime** in the top menu -> **Change runtime type**.
2. Under **Hardware accelerator**, select **GPU** (T4 GPU).
3. Click **Save**.

### Step 3: Run All Cells
1. Click **Runtime** -> **Run all** (or press `Ctrl + F9`).
2. Google Colab will prompt you: *"Permit this notebook to access your Google Drive files?"* -> Click **Connect to Google Drive**.

---

## ⚙️ What the Notebook Does Automatically

1. **Mounts Google Drive** and locates your 12 GeoTIFF files and the RGI 14 zip file.
2. **Unzips RGI 14** onto Colab's fast local SSD.
3. **Performs Geospatial Rasterization**: Matches glacier vector outlines with the Sentinel-2 10m grid and creates true binary masks (`1` for glacier, `0` for background).
4. **Extracts Real 8-Channel $256 \times 256$ Patches**: Normalized across all 8 bands (B2, B3, B4, B8, B11, B12, NDSI, NDVI) and splits 80% train / 20% val.
5. **Trains all 3 models on GPU (25 Epochs)**:
   - **U-Net (Baseline)**
   - **Attention U-Net**
   - **SUNet (Swin-UNet)**
6. **Evaluates Metrics**: Dice Score, IoU, Precision, and Recall at the optimal threshold (0.70).
7. **Saves Everything to Google Drive**:
   - Saves metrics to `MyDrive/Minor_Project/results_real_sentinel2/comparative_metrics_real_sentinel2.csv`
   - Saves performance bar charts to `comparative_metrics_chart.png`
   - Saves side-by-side false-color satellite overlays to `comparative_predictions_overlay.png`
   - Saves best `.pth` checkpoints for all 3 models.
