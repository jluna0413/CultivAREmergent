# Cannabis Dataset Acquisition Guide

## 🎯 Overview

This guide provides direct links and instructions for accessing **academic and scientific cannabis datasets** to supplement the public Hugging Face datasets.

---

## 📚 Academic Repositories

### 1. **USDA GRIN-Global** (Government - FREE) ⭐ **HIGHEST PRIORITY**

**What**: Official U.S. government hemp phenotyping database  
**Data**: Standardized descriptors for architectural traits, flowering, cannabinoids, seeds, fiber

**How to Access**:
```
1. Visit: https://npgsweb.ars-grin.gov/gringlobal/search
2. Search term: "Cannabis sativa" or "hemp"
3. Filter by:
   - Genus: Cannabis
   - Species: sativa
4. Download phenotyping data (CSV/Excel)
5. Academic use: FREE, no registration required
```

**Data Format**: Structured CSV with standardized descriptors  
**Size**: 1,000+ accessions with detailed phenotypic data

**Cornell Partnership**:
- Cornell Cooperative Extension hemp research data
- Visit: https://hemp.cals.cornell.edu/

---

### 2. **Zenodo** (Open Science - FREE)

#### DiaMOS Plant Dataset
**DOI**: Search "DiaMOS Plant Dataset" on zenodo.org  
**Data**: Plant leaf diseases with severity labels

```
1. Visit: https://zenodo.org
2. Search: "DiaMOS Plant Dataset"
3. Download: ZIP file (~2-5 GB)
4. License: CC BY 4.0 (free use with attribution)
```

#### Web-Sourced Plant Disease Dataset
**Institution**: Nottingham Trent University  
**Data**: Real-world plant images with diverse conditions

```
1. Visit: https://zenodo.org
2. Search: "plant disease detection Nottingham"
3. Download: Available under open license
```

---

### 3. **Figshare** (Academic - FREE)

#### University of Adelaide Industrial Hemp Dataset
**Direct Link**: https://figshare.com/articles/dataset/Data_for_phenotyping_of_industrial_hemp_Cannabis_sativa_L_experiments/

**Data**:
- Environmental conditions
- Growth stages
- Water stress responses
- Genotype comparisons

```
1. Visit link above
2. Click "Download all"
3. Format: CSV + metadata
4. License: CC BY (free with attribution)
```

#### Cannabis sativa Annotation Dataset
**Search**: "Cannabis sativa annotation" on figshare.com  
**Data**: Medicinal hemp breeding phenotypes

---

### 4. **NIH/PubMed Central** (Scientific Papers - FREE)

#### Hyperspectral Imaging Dataset

**Paper**: "Hyperspectral Imaging for Industrial Hemp Classification"  
**Search**: PubMed PMC, search "hyperspectral hemp Cannabis cultivation"

```
1. Visit: https://www.ncbi.nlm.nih.gov/pmc/
2. Search: "hyperspectral imaging industrial hemp machine learning"
3. Find paper with dataset link in supplementary materials
4. Download supplementary data files (often .zip with images)
```

**Data**: High-resolution spectral images of hemp cultivars

---

### 5. **Midwestern Hemp Database** (University Consortium - FREE)

**Institutions**: University of Wisconsin, Illinois, Purdue  
**URL**: https://hemp.extension.wisc.edu/

**Data**:
- Agronomic performance (yield, flowering date)
- Cannabinoid profiles (CBD, THC levels)
- Production practices
- Regional adaptation

```
1. Visit: https://hemp.extension.wisc.edu/mhd/
2. Register (free, email required)
3. Access data browser
4. Export CSV files
```

---

### 6. **Kannapedia®** (Genetics Database - FREE)

**URL**: https://www.kannapedia.net/  
**Data**: Cannabis genetic information, cultivar reports

```
1. Create free account
2. Access cultivar database
3. Export strain characteristics
4. Use for conversational context training
```

---

### 7. **ResearchGate Datasets** (Academic - FREE)

#### Cannabis Seed Image Dataset

**Search**: "Dataset of cannabis seeds for machine learning" on ResearchGate

```
1. Visit: https://www.researchgate.net
2. Search: "cannabis seed dataset machine learning"
3. Request access from authors (usually granted within 24h)
4. Download images + labels
```

#### Hemp Disease Detection Papers

**Search terms**:
- "Hemp Disease Detection Machine Learning"
- "Cannabis nutrient deficiency deep learning"
- "Cannabis pest identification dataset"

**Process**:
1. Find papers with datasets
2. Check supplementary materials
3. Contact authors if dataset not public (academic courtesy)

---

### 8. **Roboflow Universe** (Community - FREE)

**URL**: https://universe.roboflow.com/

**Search**: "cannabis" or "hemp"

```
1. Visit Roboflow Universe
2. Search: "cannabis diseases" or "hemp detection"
3. Example: "Cannabis diseases Object Detection Dataset"
4. Download in COCO, YOLO, or Pascal VOC format
5. License: Check individual datasets (most are CC BY)
```

---

### 9. **Kaggle** (Data Science - FREE)

#### Leaf Manifestation Diseases of Cannabis
**URL**: https://www.kaggle.com/datasets/...

```
1. Visit Kaggle
2. Search: "cannabis diseases" or "hemp leaves"
3. Datasets available:
   - Leaf Manifestation Diseases of Cannabis
   - Cannabis strain metadata (from Leafly)
4. Download via Kaggle API or browser
```

**Kaggle API Download**:
```bash
kaggle datasets download -d [dataset-path]
```

---

### 10. **IEEE Xplore** (Academic Papers - SUBSCRIPTION or FREE via University)

**Access Options**:
1. University library access (free for students)
2. Public library partnership (some libraries offer free access)
3. Individual papers: $33 each

**Search Strategy**:
```
1. Search: "cannabis cultivation machine learning dataset"
2. Filter: Conference Papers (more likely to have datasets)
3. Look for "Supplementary Materials" or "Dataset Availability"
4. Contact authors directly for dataset access
```

**Relevant Papers**:
- "AI Innovations in Cannabis Grading Systems"
- "Machine Learning for Hemp Disease Detection"

---

### 11. **arXiv** (Preprints - FREE)

**URL**: https://arxiv.org/

**Cannabis/Hemp ML Papers**:
```
1. Search: "cannabis machine learning" or "hemp computer vision"
2. Look for papers with datasets in supplementary materials
3. Download paper + check for dataset links
```

**Recent Topics**:
- Computer vision for plant phenotyping
- ML for disease classification
- Automated quality grading

---

## 📋 Acquisition Checklist

### Week 1: Foundation Datasets
- [ ] PlantVillage (Kaggle)
- [ ] PlantDoc (Hugging Face)
- [ ] DiaMOS (Zenodo)
- [ ] USDA GRIN-Global hemp data

### Week 2: Cannabis-Specific
- [ ] University of Adelaide (Figshare)
- [ ] Midwestern Hemp Database
- [ ] Roboflow cannabis datasets
- [ ] Kaggle cannabis leaf diseases

### Week 3: Advanced/Optional
- [ ] Hyperspectral imaging (NIH/PubMed)
- [ ] ResearchGate seed dataset
- [ ] Kannapedia genomics data
- [ ] IEEE/arXiv supplementary datasets

---

## 🔄 Data Integration Workflow

### 1. Download
```bash
# Create organized directory
mkdir -p ml/datasets/academic
cd ml/datasets/academic

# Subdirectories by source
mkdir usda zenodo figshare nih kaggle researchgate
```

### 2. Organize
```
ml/datasets/academic/
├── usda/
│   └── hemp_phenotyping_data.csv
├── zenodo/
│   ├── diamos_plant_dataset/
│   └── web_sourced_diseases/
├── figshare/
│   └── adelaide_hemp_phenotypes/
├── nih/
│   └── hyperspectral_hemp/
├── kaggle/
│   └── cannabis_leaf_diseases/
└── researchgate/
    └── cannabis_seeds/
```

### 3. Preprocess
```python
# Use dataset curator tool
python ml/tools/dataset_curator.py --import academic

# Or manually integrate with training pipeline
```

---

## 📊 Expected Dataset Stats

After acquiring all sources:

| Source | Images | Type | Size |
|--------|--------|------|------|
| USDA GRIN-Global | N/A | Tabular | ~50 MB |
| Zenodo (DiaMOS) | ~10K | Images | ~5 GB |
| Figshare (Adelaide) | ~2K | Images + Data | ~1 GB |
| NIH Hyperspectral | ~500 | Spectral | ~2 GB |
| Midwestern Hemp | N/A | Tabular | ~10 MB |
| Roboflow | ~1K | Annotated Images | ~500 MB |
| Kaggle Cannabis | ~2K | Images | ~1 GB |
| **TOTAL** | **~15K cannabis-specific** | **Mixed** | **~10 GB** |

Combined with Hugging Face datasets (PlantVillage, PlantWild, LeafNet):
- **Total Images**: 200K+
- **Cannabis-Specific**: 15K+
- **Total Size**: ~25 GB

---

## 📝 Usage Notes

### Attribution Requirements

When using academic datasets:
```markdown
This model was trained using data from:
- USDA-ARS Plant Genetic Resources Unit (Public Domain)
- University of Adelaide Industrial Hemp Dataset (CC BY 4.0)
- DiaMOS Plant Dataset, Zenodo (CC BY 4.0)
- [List others as applicable]
```

### Data Cleaning

Academic datasets may need preprocessing:
1. **Format standardization**: Convert all to common format (COCO JSON)
2. **Label mapping**: Map academic terms to your taxonomy
3. **Quality filtering**: Remove corrupted/mislabeled images
4. **Augmentation**: Apply transforms for diversity

---

## 🤝 Collaboration Opportunities

Consider reaching out to researchers for:
- Latest unpublished datasets
- Collaboration on model validation
- Co-authorship on papers using CultivAR
- Access to private research datasets

**Contact Template**:
```
Subject: Research Collaboration - Cannabis Plant Health ML

Dear Dr. [Name],

I'm developing an open-source AI system for cannabis cultivation 
health monitoring (CultivAR). I came across your work on [topic] 
and was wondering if you'd be interested in collaboration or if 
your dataset might be available for academic use.

[Your credentials/affiliation]
```

---

## ✅ Quick Start

**Fastest path to quality cannabis data** (1-2 hours):

```bash
# 1. USDA GRIN-Global (30 min)
wget [USDA download link from search]

# 2. Figshare Adelaide dataset (20 min)
wget https://figshare.com/ndownloader/files/[file-id]

# 3. Roboflow cannabis diseases (10 min)
# Via browser download

# 4. Start training with these + PlantVillage
python ml/fine_tuning/prepare_datasets.py --sources usda figshare roboflow plantvillage
```

You now have government-verified + academic cannabis data ready for fine-tuning! 🌿
