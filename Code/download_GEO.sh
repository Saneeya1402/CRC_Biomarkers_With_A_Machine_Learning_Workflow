#!/usr/bin/env bash
#
# download_GEO.sh
# A clean, automated script to download raw GEO files required for:
#         CRC_Biomarkers_With_A_Machine_Learning_Workflow
#
# Downloads:
#   - GSE103512 series matrix (expression data)
#   - GPL13158 platform annotation (probe → gene mapping)
#
# Output:
#   Data/Raw/GSE103512_series_matrix.txt.gz
#   Data/Raw/GPL13158.annot.gz
#
# Usage:
#   bash download_GEO.sh
#
# --------------------------------------------------------------

set -e  # Exit immediately if a command exits with a non-zero status

# Pretty colors for terminal output
GREEN="\033[0;32m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # No color

echo -e "${BLUE}\n============================================="
echo -e "  GEO Data Downloader for CRC Biomarker Project"
echo -e "=============================================${NC}"

# Create necessary folder structure
# Determine the directory where this script lives
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# The repo root is one level up from Code/
REPO_ROOT="$( dirname "$SCRIPT_DIR" )"

# Data folder should be at the repo root
RAW_DIR="$REPO_ROOT/Data/Raw"
mkdir -p "$RAW_DIR"

echo -e "${GREEN}[1/4] Creating folder structure...${NC}"
echo "→ Ensured $RAW_DIR exists."

# GEO URLs
GSE_URL="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE103nnn/GSE103512/matrix/GSE103512_series_matrix.txt.gz"
GPL_URL="https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL13nnn/GPL13158/annot/GPL13158.annot.gz"

echo -e "${GREEN}[2/4] Preparing to download GEO files...${NC}"
echo "Files to download:"
echo "  - $GSE_URL"
echo "  - $GPL_URL"
echo ""

# Check if wget or curl is installed
if command -v wget >/dev/null 2>&1; then
    DOWNLOADER="wget -O"
elif command -v curl >/dev/null 2>&1; then
    DOWNLOADER="curl -L -o"
else
    echo -e "${RED}Error: Neither wget nor curl is installed.${NC}"
    echo "Please install one of them and re-run this script."
    exit 1
fi

# Download GSE103512 Series Matrix
echo -e "${GREEN}[3/4] Downloading GSE103512 Series Matrix...${NC}"
$DOWNLOADER "$RAW_DIR/GSE103512_series_matrix.txt.gz" "$GSE_URL"

if [ -f "$RAW_DIR/GSE103512_series_matrix.txt.gz" ]; then
    echo "✓ Successfully downloaded GSE103512_series_matrix.txt.gz"
else
    echo -e "${RED}✗ Failed to download GSE103512 series matrix.${NC}"
    exit 1
fi

# Download GPL13158 Annotation File
echo -e "${GREEN}[4/4] Downloading GPL13158 Annotation File...${NC}"
$DOWNLOADER "$RAW_DIR/GPL13158.annot.gz" "$GPL_URL"

if [ -f "$RAW_DIR/GPL13158.annot.gz" ]; then
    echo "✓ Successfully downloaded GPL13158.annot.gz"
else
    echo -e "${RED}✗ Failed to download GPL13158 annotation file.${NC}"
    exit 1
fi

echo -e "${BLUE}\n============================================="
echo -e "   All GEO files downloaded successfully!"
echo -e "   Files saved to: $RAW_DIR/"
echo -e "   You can now run:"
echo -e "       python Code/prepare_data.py"
echo -e "=============================================${NC}\n"

