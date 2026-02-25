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
Due to file size limits, large models and datasets are hosted on **Hugging Face**: [style-transfer-artifact/OtakuLab · Hugging Face](https://huggingface.co/style-transfer-artifact/OtakuLab).

### Models (Hugging Face / ModelScope)
| Path | Description | Link |
|------|-------------|------|
| `outputs/model/styled-qwen` | **Styled-Qwen3-1.7B (Model V1)** <br> The main fine-tuned model with style vector support. | [style-transfer-artifact/OtakuLab at main](https://huggingface.co/style-transfer-artifact/OtakuLab/tree/main/outputs/model/styled-qwen) |
| `outputs/model/styled-qwen-balanced` | **Styled-Qwen3-1.7B (Model V2)** | [style-transfer-artifact/OtakuLab at main](https://huggingface.co/style-transfer-artifact/OtakuLab/tree/main/outputs/model/styled-qwen-balanced) |
| `outputs/style-classifier/` | **Style Classifier (RoBERTa)** <br> Fine-tuned classifier for style consistency evaluation. | [style-transfer-artifact/OtakuLab at main](https://huggingface.co/style-transfer-artifact/OtakuLab/tree/main/outputs/style-classifier) |

### Datasets (Hugging Face Datasets)
| Path | Description | Link |
|------|-------------|------|
| `outputs/cons/psydc.json` | **PsyDC Parse Trees** <br> Large-scale constituency parse trees (>150MB). | [outputs/cons/psydc.json · style-transfer-artifact/OtakuLab at main](https://huggingface.co/style-transfer-artifact/OtakuLab/blob/main/outputs/cons/psydc.json) |

## 🏗️ Reproducible Locally
The following files are excluded but can be reproduced by running the notebooks:

*   **`outputs/tokens/*.pkl`**: Intermediate tokenization cache. 
    *   *To reproduce*: Run `notebooks/11_feature_pmi_builder.ipynb`.
