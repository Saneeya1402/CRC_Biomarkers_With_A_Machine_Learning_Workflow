# 🧬 CRC_Biomarkers_With_A_Machine_Learning_Workflow

*A reproducible Python-based pipeline for colorectal cancer biomarker discovery*


## Overview

This repository contains a complete, step-wise reconstruction of a published bioinformatics and machine learning workflow used to identify potential biomarkers for colorectal cancer (CRC) using microarray gene expression data.
The workflow is based on the study: 

*Hammad, A., Elshaer, M., & Tang, X. (2021). Identification of potential biomarkers with colorectal cancer based on bioinformatics analysis and machine learning. Mathematical Biosciences & Engineering, 18(6), 8997–9015.*

Colorectal cancer is one of the most common and deadly cancers worldwide. Early detection depends heavily on reliable molecular biomarkers, but traditional approaches often suffer from noise, small sample sizes, and inconsistent findings. This project reconstructs the major bioinformatics components of the published workflow:

- Mapping Affymetrix probe IDs → gene symbols
- Collapsing multiple probes per gene
- Differential gene expression (Tumor vs Normal)
- Log2 fold change calculations
- t-tests and Benjamini–Hochberg FDR correction
- Identification of upregulated and downregulated genes
- Visualization using:
- Volcano plot (significance vs fold change)
- Heatmap of significant DEGs (Euclidean distance, average linkage)

Although the original study also included classifier development (SVM, ROC curves), this repository focuses specifically on the bioinformatics + statistical pipeline, which is the foundation for downstream ML.
The project walks through data acquisition, preprocessing, probe-to-gene mapping, differential gene expression analysis, and visualization through both a volcano plot and a hierarchical clustered heatmap, replicating Figures 2B and 2C from the publication.


## 📂 Repository Structure

```r
CRC_Biomarkers_With_A_Machine_Learning_Workflow/
│
├── Data/
│   └── How_to_Download_and_Prepare_Data.txt      # Step-by-step guide for obtaining GEO data
│
├── Code/
│   ├── CRC_ML_Notebook.ipynb                     # Main Python notebook
│   └── README_Code_Explanation.txt               # What each code block does, step-by-step
│
└── Results/
    ├── volcano_plot.png                           # Placeholder
    ├── heatmap.png                                # Placeholder
    └── README_Results.txt                         # Explanation of expected outputs
```


## ⚙️ Technologies Used

- **Python 3**
- **NumPy** – numerical operations  
- **Pandas** – data manipulation and preprocessing  
- **SciPy** – statistical testing (t-tests)  
- **statsmodels** – Benjamini–Hochberg FDR correction  
- **Matplotlib** – plotting  
- **Seaborn** – volcano plot and heatmap visualization  
- **scikit-learn** – scaling for clustering  
- **SciPy Hierarchical Clustering** – Euclidean distance + average linkage




## 💻📦 Installation & Requirements

This project uses Python and common scientific computing libraries.  
To run the full workflow, you will need:

### **✔ Python Version**
- Python **3.8 or higher**

### **✔ Required Python Packages**

- numpy  
- pandas  
- scipy  
- statsmodels  
- matplotlib  
- seaborn  
- scikit-learn  

You can install all dependencies using either **pip** or **conda**.

---

### **Option 1 — Install via `pip`**

```bash
pip install numpy pandas scipy statsmodels matplotlib seaborn scikit-learn
```

### **Option 2 — Install via Conda (Recommended)**

```bash
conda install numpy pandas scipy statsmodels matplotlib seaborn scikit-learn
```
### Cloning the Repository

```bash
git clone https://github.com/<your-username>/CRC_Biomarkers_With_A_Machine_Learning_Workflow.git
cd CRC_Biomarkers_With_A_Machine_Learning_Workflow
```




## ▶️ How to Use This Repository

Because GEO data is large and cannot be stored directly in this repository:

1. Navigate to:  
   **`Data/How_to_Download_and_Prepare_Data.txt`**  
   This file contains detailed, step-by-step instructions for downloading:
   - **GSE103512** microarray expression matrix  
   - **GPL13158** probe annotation platform  
   - How to create the **metadata file** manually  
   - How to prepare all inputs required for the notebook

2. Open the notebook inside the `Code/` folder:  
   **`Code/CRC_ML_Notebook.ipynb`**  
   Follow the workflow from probe mapping → collapsing probes → DGE → volcano and heatmap generation.

3. For a human-readable walkthrough, refer to:  
   **`Code/README_Code_Explanation.txt`**  
   This file explains each section of the notebook in clear, step-wise language.

4. When run with the real GEO data, the notebook will save outputs into the `Results/` folder.



## 🔍 Expected Outputs

Although the actual data-derived images are not included (due to size and GEO redistribution restrictions), the workflow normally produces:

### **✔ Volcano Plot**
- Shows log2 fold change vs −log10(adjusted p-value)  
- Color coding:
  - **Red** – significantly upregulated genes  
  - **Blue** – significantly downregulated genes  
- Thresholds used:  
  - `|log2FC| > 1.5`  
  - `adjusted p-value < 0.05`

### **✔ Hierarchical Heatmap**
- Displays expression of significant DEGs across all samples  
- Clustering:
  - **Rows (genes)** – Euclidean distance, average linkage  
  - **Columns (samples)** – grouped by Tumor vs Normal  
- Demonstrates clear separation between tumor and normal expression profiles  
- Replicates Figure 2B from the original study

The `Results/` folder contains placeholders and explanations describing these outputs.



## 📚 Citation

If you use or reference this workflow, please cite the original publication:

**Hammad, A., Elshaer, M., & Tang, X. (2021). Identification of potential biomarkers with colorectal cancer based on bioinformatics analysis and machine learning. _Mathematical Biosciences & Engineering_, 18(6), 8997–9015.**  
https://doi.org/10.3934/mbe.2021443



## 🧵 Notes

- This repository intentionally does **not** include raw GEO data due to GitHub storage limits and GEO redistribution rules.
- The project is structured to be **portfolio-friendly**, highlighting:
  - Bioinformatics pipeline skills  
  - Data wrangling and preprocessing  
  - Differential expression analysis  
  - Clustering and visualization  
  - Ability to reproduce a published scientific workflow  
- The workflow mirrors Figures **2B** and **2C** from the publication using Python.

---

### *The emojis' are not from ChatGPT, I just like them! Thank you!
