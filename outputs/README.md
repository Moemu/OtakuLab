# OtakuLab Outputs

This directory contains the experimental results and model artifacts for the paper.

## 📂 Included in Repository
The following lightweight results are directly included in this repository for reproducibility:

*   **`pmi/`**: Extracted style keywords (JSON).
*   **`pragmatic/`**: Pragmatic style analysis results (JSONL).
*   **`rag/`**: FAISS indexes and corpuses for RAG evaluation.
*   **`meta_learner/`**: Lightweight meta-learner models (PyTorch `.pth`).
*   **`cons/`**: Constituency parse trees (JSON) for most styles (except PsyDC).

## ☁️ Hosted on External Platforms

Due to file size limits, large models and datasets are hosted on External Platforms.

It will be released upon acceptance.

## 🏗️ Reproducible Locally
The following files are excluded but can be reproduced by running the notebooks:

*   **`outputs/tokens/*.pkl`**: Intermediate tokenization cache. 
    *   *To reproduce*: Run `notebooks/11_feature_pmi_builder.ipynb`.
