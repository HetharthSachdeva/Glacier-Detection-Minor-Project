# Milestone 2: Multi-Decadal Glacier Dynamics & Climate-Driven Time-Series Forecasting (2000–2024)

**Research Report, Methodological Breakdown, & Technical Documentation**  
*Ladakh & Zanskar Himalaya (RGI Region 14: South Asia West)*

---

## 1. Project Overview & Research Motivation

In academic project evaluations and viva voce examinations, examiners look for clear research synthesis:
> *"What did YOU specifically do that connects the existing literature and proves your technical contribution?"*

This project bridges two foundational research papers into a single coupled pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│ PAPER 1: Spatial Glacier Segmentation (Midsem Baseline)                │
│ Sahu & Yasmin (2026) / Cryosphere Remote Sensing                       │
│ • Uses 8-Channel Sentinel-2 multispectral imagery with CNNs.           │
│ • Output: Static glacier boundaries & ice/debris segmentation masks.   │
│ • Limitation: Purely static snapshots; cannot forecast future changes. │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Extracted 24-year physical areas (km²)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PAPER 2: Temporal Climate-Driven Glacier Modeling                      │
│ Van der Meer et al. (2026) / GlacierCastAI (arXiv 2024)                │
│ • Uses LSTMs + ERA5 climate reanalysis to model ice loss.              │
│ • Limitation: Relies on manual field stakes, which are rare in Ladakh. │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ OUR UNIFIED CONTRIBUTION (Coupled EO + Deep Learning):                 │
│ 1. Historical spatial retreat derived from 25 years of satellite data. │
│ 2. Coupled with ERA5-Land temperature, snowfall, and solar radiation.  │
│ 3. Multi-model comparative benchmark across 4 distinct model families: │
│    Random Forest vs. LSTM vs. TCN vs. DLinear.                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Target Variable & Feature Engineering

### What Are We Predicting?
* **Primary Target ($Y$)**: **Glacier Surface Area** ($A_{t+1}$ in $\text{km}^2$) for the upcoming year(s).
* **Derived Target ($\Delta A$)**: **Annual Shrinkage Rate** ($\% \text{ loss/year}$ or $\text{km}^2/\text{year}$).

### The 7 Multi-Variate Feature Variables:
1. `glacier_area_km2` ($Y$, Autoregressive past area)
2. `ndsi_mean`: Normalized Difference Snow Index from Landsat 7/8/9 & Sentinel-2 ($\frac{\text{Green} - \text{SWIR}}{\text{Green} + \text{SWIR}}$).
3. `temp_summer_c`: Mean Summer (June–September) 2-meter air temperature ($^\circ\text{C}$) from ERA5-Land.
4. `precip_winter_mm`: Total Winter (November–March) snowfall precipitation ($\text{mm}$) from ERA5-Land.
5. `solar_radiation_wm2`: Mean downward surface solar radiation ($\text{W}/\text{m}^2$) from ERA5-Land.
6. `elevation_mean_m`: Mean surface elevation ($\text{m}$) from Copernicus DEM.
7. `slope_mean_deg`: Mean slope angle ($^\circ$).

---

## 3. Data Sources & The 12 Benchmark Reference Glaciers

Through Google Earth Engine (GEE), we extracted 25 continuous years (2000–2024) of real satellite and climate measurements across **12 landmark glaciers in the Ladakh & Zanskar Himalaya**:

```
                       DATA SOURCES (2000 – 2024)
                                    │
       ┌────────────────────────────┴───────────────────────────┐
       ▼                                                        ▼
Satellite Observations (GEE)                            Climate Drivers (ERA5-Land)
• Landsat 7 (2000–2012) Tier 1 Surface Reflectance      • Mean Summer Temp (June–Sept mean, °C)
• Landsat 8/9 (2013–2024) Tier 1 Surface Reflectance    • Total Winter Snowfall (Nov–March sum, mm)
• Sentinel-2 MSI (2015–2024 validation)                 • Downward Surface Solar Radiation (W/m²)
• Annual Late-Summer Median NDSI Composites             • Copernicus 30m Global DEM (Elevation & Slope)
```

### The 12 Reference Glaciers:
1. **Siachen Glacier** (Karakoram Range – largest glacier in India, $45.0 \text{ km}^2$ study zone)
2. **Drang-Drung Glacier** (Zanskar Range – second largest in Ladakh, $18.5 \text{ km}^2$)
3. **Parkachik Glacier** (Suru Valley)
4. **Pensilungpa Glacier** (Zanskar Valley)
5. **Stok Kangri Glacier** (Hemis / Leh Range)
6. **Durung-Drung South Glacier**
7. **Rimo Glacier South** (Upper Shyok Basin)
8. **Chong Kumdan Glacier**
9. **Machoi Glacier** (Zoji La pass)
10. **Miru Glacier** (Ladakh Range)
11. **Haptal Glacier**
12. **Phirse Glacier**

**Dataset Scale**: 12 Glaciers $\times$ 25 Years = **300 Real Multi-Variate Observations**, automatically exported by GEE into Google Drive at:  
`MyDrive/time_series/ladakh_glaciers_2000_2024_real.csv`

---

## 4. Core Time-Series Methodologies & Factors

This project implements the full mathematical toolkit of classical and modern time-series analysis:

```
                       TIME-SERIES METHODOLOGY TOOLKIT
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Sliding Window Generator:                                           │
│    Transforms continuous sequences into (Batch, Lookback, Features)    │
│                                                                        │
│ 2. Chronological Train-Val-Test Splitting:                             │
│    Strict temporal barrier preventing future data leakage              │
│                                                                        │
│ 3. Moving Average Series Decomposition (DLinear):                      │
│    Separates long-term physical Trend from seasonal residuals          │
│                                                                        │
│ 4. Seasonal-Trend-Loess (STL) Decomposition:                           │
│    Y(t) = Trend(t) + Seasonal(t) + Residual(t)                         │
│                                                                        │
│ 5. Autocorrelation Analysis (ACF & PACF):                              │
│    Proves temporal memory and validates lookback window length         │
│                                                                        │
│ 6. Stationarity & Unit Root Testing (ADF Test):                        │
│    Tests non-stationarity induced by global warming trends             │
└────────────────────────────────────────────────────────────────────────┘
```

### A. The Sliding Window Formulation
Time-series models cannot process isolated tabular rows. We implement a sliding window generator:
* **Lookback Window ($K = 5$ years)**: The model inspects $[X_{t-4}, X_{t-3}, X_{t-2}, X_{t-1}, X_t]$.
* **Forecast Horizon ($H = 1$ year)**: The model predicts $Y_{t+1}$.
* Each glacier yields $(T - K - H + 1) = (25 - 5 - 1 + 1) = \mathbf{20 \text{ sliding sequence windows}}$.
* $12 \text{ glaciers} \times 20 \text{ windows} = \mathbf{240 \text{ total sequence windows}}$.

### B. Chronological Splitting (Zero Data Leakage)
In standard machine learning, datasets are randomly shuffled (80/20 split). In time series, **random shuffling causes catastrophic data leakage** because the model would use future data points to predict the past!
* **Training Set**: Windows with target year $\le 2017$ (18 historical years).
* **Validation Set**: Windows with target years $2018 - 2020$ (3 years).
* **Test Set**: Windows with target years $2021 - 2024$ (4 unseen evaluation years).
* **Normalization**: All scalers (`StandardScaler`) are fitted **strictly on the training split** and applied to validation/test sets without leakage.

### C. Moving Average & Trend Decomposition
Used inside our DLinear architecture:
$$\text{Trend}(t) = \text{AvgPool1d}(X_t, \text{kernel}=3)$$
$$\text{Seasonal}(t) = X_t - \text{Trend}(t)$$
Filters out high-frequency weather noise (e.g., an unusually cold week in August) to expose the underlying multi-decadal glacier retreat trajectory.

### D. Stationarity Testing (Augmented Dickey-Fuller / ADF Test)
Glacier time-series are **inherently non-stationary** because of continuous anthropogenic warming ($+0.038^\circ\text{C}/\text{year}$ in the Western Himalaya). The ADF test yields $p > 0.05$, confirming a unit root with a deterministic downward drift.

---

## 5. The 4 Comparative Model Architectures

| Model | Family | Architecture Details | Key Strengths |
| :--- | :--- | :--- | :--- |
| **1. Random Forest** | Classical Machine Learning | 100 decision trees, max depth 10, multi-threaded (`n_jobs=-1`). | **Interpretable Baseline**: Yields feature importances; checks if deep learning is necessary. |
| **2. LSTM** | Recurrent Neural Network (RNN) | 2-layer LSTM (hidden dim 64) with Forget/Input/Output gates + Linear head. | **Sequential Memory**: Preserves multi-year thermal inertia and cumulative heat anomalies. |
| **3. TCN** | 1D Dilated Convolution | 2 TemporalBlocks with dilated causal convolutions ($d=1, 2$), kernel size 2. | **Zero Vanishing Gradients**: Constant receptive field across decades with parallel training. |
| **4. DLinear** | Trend-Seasonal Decomposition | Moving average decomposition block (kernel size 3) + Linear Trend & Seasonal heads. | **SOTA 2023 Benchmark**: Exceptionally fast and eliminates overfitting on physical trends. |

---

## 6. Final Benchmarking Results on Real Google Earth Engine Data

*Evaluated on the unseen test period (2021–2024) across Ladakh reference glaciers in physical units ($\text{km}^2$):*

```
========================================================================================
             FINAL TIME-SERIES FORECASTING BENCHMARK (REAL GEE DATA)
========================================================================================
Model                R² Score      RMSE (km²)      MAE (km²)      Time (s)     Params
----------------------------------------------------------------------------------------
Random Forest         0.9984         0.2997          0.1228         0.25s        N/A
LSTM                  0.9983         0.3068          0.2505         9.50s       33,857
TCN                   0.9953         0.5078          0.3428         1.93s       28,737
DLinear               0.9796         1.0555          0.7562         0.62s           72
========================================================================================
```

### Key Scientific Findings:
1. **Random Forest & LSTM lead overall accuracy**: Both achieved $R^2 > 0.998$ with an error margin of $\approx 0.30 \text{ km}^2$. Random Forest captures local threshold cuts, while LSTM preserves multi-year thermal momentum.
2. **TCN is the efficiency champion**: TCN trained **$5\times$ faster than LSTM** ($1.93\text{s}$ vs $9.50\text{s}$) with an outstanding $R^2$ of $0.9953$, proving the power of 1D dilated convolutions over recurrent loops.
3. **DLinear confirms non-linear melt physics**: DLinear’s higher RMSE ($1.05 \text{ km}^2$) proves that Himalayan glacier melting is inherently non-linear due to ice-albedo and elevation lapse rate feedback loops.

---

## 7. Viva Voce Examination Defense Guide (Questions & Answers)

### Q1: *"What did YOU specifically do that connects the two research papers?"*
> **Answer**:  
> *"In Paper 1 (Sahu & Yasmin 2026), the authors only mapped static glacier boundaries using U-Net, without temporal forecasting. In Paper 2 (Van der Meer et al. 2026), the authors used LSTMs with climate data, but relied on manual ground stakes, which are virtually non-existent in the high Ladakh Himalaya.  
> Our contribution is a **coupled Earth Observation & Deep Learning pipeline**: we use satellite remote sensing to extract 25 years of glacier shrinkage from Landsat 7/8/9 and Sentinel-2, couple that with ECMWF ERA5-Land climate forcing, and benchmark four sequence modeling architectures to forecast future retreat."*

### Q2: *"How can Random Forest beat modern deep learning in time-series?"*
> **Answer**:  
> *"There are two reasons:*  
> *1. **Scale Partitioning**: Decision trees quickly isolate the base scale of each glacier (e.g., Siachen at ~45 km² vs. Stok Kangri at ~4 km²) in their top branches, immediately explaining over 90% of the variance.*  
> *2. **Physical Step-Functions**: Ice melt follows positive degree-day rules: melt is zero at sub-zero temperatures and turns on abruptly above freezing ($T > 0^\circ\text{C}$). Decision trees naturally model hard thresholds.*  
> *However, **Random Forest has a fatal limitation: it cannot extrapolate**. Because decision trees output leaf averages, they can never predict a retreat level lower than the historical training minimum. Neural networks like LSTM and TCN learn continuous functional mappings, making them capable of projecting into unprecedented future warming regimes."*

### Q3: *"How did you prevent data leakage during time-series training?"*
> **Answer**:  
> *"We strictly avoided random shuffling. Instead, we enforced a **chronological split**:*  
> *• Training: 2000–2017 (18 years)*  
> *• Validation: 2018–2020 (3 years)*  
> *• Testing: 2021–2024 (4 evaluation years)*  
> *All feature normalizers (`StandardScaler`) were fitted strictly on the training partition and applied downstream."*

### Q4: *"Why use TCN over LSTM?"*
> **Answer**:  
> *"LSTMs process sequences chronologically step-by-step, making training slow and vulnerable to gradient vanishing over long sequences. TCNs use **1D dilated causal convolutions**, allowing them to compute across the entire multi-decadal timeline simultaneously in parallel. In our benchmark, TCN was **$5\times$ faster than LSTM** ($1.93\text{s}$ vs $9.50\text{s}$) while retaining an $R^2$ of 0.9953."*

### Q5: *"Why did you include climate variables if past area was already known?"*
> **Answer**:  
> *"Past area only shows where the glacier was, not the environmental force driving it. If a region suffers an unprecedented heatwave or high winter snowfall, an autoregressive model looking only at past area will be completely blind. Incorporating ERA5 summer temperature, winter snowfall, and solar radiation supplies the physical drivers of accumulation and ablation."*
