#!/usr/bin/env python3
"""
prepare_data.py
-----------------------------------------
Automates preprocessing of raw GEO data for:

    CRC_Biomarkers_With_A_Machine_Learning_Workflow

This script performs:

1. Extraction of the expression matrix from:
      Data/Raw/GSE103512_series_matrix.txt.gz

2. Extraction of probe → gene mapping from:
      Data/Raw/GPL13158.annot.gz

3. Automatic generation of metadata (Tumor vs Normal)
      using sample characteristics from the series matrix file.

Outputs are saved into:
      Data/Processed/raw_counts.csv
      Data/Processed/probe_to_gene.csv
      Data/Processed/metadata.csv

Usage:
      python Code/prepare_data.py
-----------------------------------------
"""

import os
import gzip
import pandas as pd
import numpy as np
import re
from io import StringIO

# ------------------------------------------------------------
# Helper: find repo root
# ------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

RAW_DIR = os.path.join(REPO_ROOT, "Data", "Raw")
PROCESSED_DIR = os.path.join(REPO_ROOT, "Data", "Processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)


print("\n===============================================")
print("  PREPARING GEO DATA FOR CRC BIOMARKER PROJECT")
print("===============================================\n")


# ------------------------------------------------------------
# 1. Process GSE103512 expression matrix
# ------------------------------------------------------------
series_matrix_path = os.path.join(RAW_DIR, "GSE103512_series_matrix.txt.gz")

if not os.path.exists(series_matrix_path):
    raise FileNotFoundError(
        f"ERROR: {series_matrix_path} not found.\n"
        "Run download_GEO.sh first."
    )

print("[1/3] Extracting expression matrix from series matrix file...")


# Step 1A — Read file, find where table starts and ends
with gzip.open(series_matrix_path, "rt") as f:
    lines = f.readlines()

# Locate table boundaries
table_start = None
table_end = None

for i, line in enumerate(lines):
    if line.startswith("!series_matrix_table_begin"):
        table_start = i + 1
    elif line.startswith("!series_matrix_table_end"):
        table_end = i
        break

if table_start is None or table_end is None:
    raise ValueError("ERROR: Could not locate expression table in series matrix.")

# Extract only the expression table
table_lines = lines[table_start:table_end]

# Convert to a dataframe

expr_df = pd.read_csv(
    StringIO("".join(table_lines)),
    sep="\t"
)

# Rename ID_REF to ProbeID
expr_df = expr_df.rename(columns={"ID_REF": "ProbeID"})

# Save clean expression matrix
raw_counts_path = os.path.join(PROCESSED_DIR, "raw_counts.csv")
expr_df.to_csv(raw_counts_path, index=False)

print(f"✓ Saved cleaned expression matrix → {raw_counts_path}")


# ------------------------------------------------------------
# 2. Process GPL13158 annotation file
# ------------------------------------------------------------
annot_path = os.path.join(RAW_DIR, "GPL13158.annot.gz")

if not os.path.exists(annot_path):
    raise FileNotFoundError(
        f"ERROR: {annot_path} not found.\n"
        "Run download_GEO.sh first."
    )

print("[2/3] Processing GPL13158 annotation file...")

# Read entire annotation file
with gzip.open(annot_path, "rt", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Identify platform table section
start = None
end = None

for i, line in enumerate(lines):
    if line.startswith("!platform_table_begin"):
        start = i + 1
    elif line.startswith("!platform_table_end"):
        end = i
        break

if start is None or end is None:
    raise ValueError("Could not find platform table inside GPL file")

# Extract only the table section
table_section = "".join(lines[start:end])

from io import StringIO
annot_df = pd.read_csv(StringIO(table_section), sep="\t", dtype=str)

# Clean column names
annot_df.columns = annot_df.columns.str.strip()

# Dynamically detect possible gene symbol columns
gene_cols = ["Gene symbol", "gene_symbol", "GENE_SYMBOL", "Gene.symbol", "Symbol"]
gene_col = None
for col in gene_cols:
    if col in annot_df.columns:
        gene_col = col
        break

if gene_col is None:
    raise ValueError("No Gene Symbol column found in annotation file")

# Detect possible Entrez ID columns
entrez_cols = ["Gene ID", "ENTREZ_GENE_ID", "Entrez Gene", "EntrezID"]
entrez_col = None
for col in entrez_cols:
    if col in annot_df.columns:
        entrez_col = col
        break

if entrez_col is None:
    print("⚠ No Entrez ID column found — filling with 'NA'")
    annot_df["ENTREZ_GENE_ID"] = "NA"
    entrez_col = "ENTREZ_GENE_ID"

# Build final annotation table
final_annot = annot_df[["ID", gene_col, entrez_col]].copy()
final_annot.columns = ["ProbeID", "Gene Symbol", "ENTREZ_GENE_ID"]

# Save
probe_to_gene_path = os.path.join(PROCESSED_DIR, "probe_to_gene.csv")
final_annot.to_csv(probe_to_gene_path, index=False)

print(f"✓ Saved annotation → {probe_to_gene_path}")


# ------------------------------------------------------------
# 3. Auto-generate metadata.csv (Tumor vs Normal)
# ------------------------------------------------------------


print("[3/3] Extracting metadata from series matrix file...")

# Use the existing series matrix path variable
matrix_path = series_matrix_path

sample_ids = []
sample_normals = []

# Read the gzipped file
import gzip
with gzip.open(matrix_path, "rt", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Extract sample IDs (GSM IDs)
for line in lines:
    if line.startswith("!Sample_geo_accession"):
        parts = line.strip().split("\t")
        sample_ids = parts[1:]   # All sample GSM IDs
        break

# Extract normal/tumor from characteristics
for line in lines:
    if line.startswith("!Sample_characteristics_ch1"):
        parts = line.strip().split("\t")[1:]
        for entry in parts:
            entry = entry.replace('"', '').strip().lower()
            if "normal: yes" in entry:
                sample_normals.append("Normal")
            elif "normal: no" in entry:
                sample_normals.append("Tumor")
            else:
                sample_normals.append("Unknown")
        break

# Build metadata DataFrame
metadata_df = pd.DataFrame({
    "SampleID": sample_ids,
    "SampleType": sample_normals
})

# Save metadata
metadata_path = os.path.join(PROCESSED_DIR, "metadata.csv")
metadata_df.to_csv(metadata_path, index=False)

print("✓ Metadata extracted and saved →", metadata_path)
print(metadata_df.head())
print(metadata_df['SampleType'].value_counts())


print("   All data prepared successfully!")
print("   Processed files saved in Data/Processed/")
print("===============================================\n")

