# OtakuLab

OtakuLab is the experimental codebase for reproducing the results of the paper. It contains the complete workflow from data cleaning, feature extraction (PMI, PCFG, Pragmatic vectors), model fine-tuning (Styled-Qwen), to automated evaluation.

## Project Structure

Verified and reorganized directory structure:

```
OtakuLab/
├── data/               # Raw and processed datasets (JSONL)
├── notebooks/          # Step-by-step experiment notebooks
├── outputs/            # Experiment inputs/outputs (Models, Logs, Indexes)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Key Directories
*   **`data/`**: contains the Haruhi, Muice, and generated neutral sentence datasets.
*   **`outputs/`**: stores the trained style classifiers, FAISS vector indexes, and large language model adapters (LoRA). *Note: Large model files will be released upon acceptance. (see `outputs/README_OUTPUTS.md`).*
*   **`notebooks/`**: contains all executable code, numbered by execution order.

## Outputs & Models

Due to file size limits, large model weights (e.g., `outputs/model/styled-qwen`) are not included in this repo. And it will be released upon acceptance.

## Environmental Setup

This project uses **Conda** for environment management.

1.  **Create Conda Environment**:
    ```bash
    conda create -n Paper python=3.12
    conda activate Paper
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    *Note: For GPU support with `torch` and `faiss`, ensure you install the CUDA versions appropriate for your system.*

## Reproducibility Workflow

The notebooks are numbered to indicate the correct execution order. Please run them in the following sequence:

### 1: Data Preparation (Optional)
*   `01_dataset_clean_haruhi.ipynb`: Clean the raw Haruhi dataset.
*   `02_dataset_gen_neutral_train.ipynb`: Generate neutral training sentences.

### 2: Feature Engineering (Optional)
*   `11_feature_pmi_builder.ipynb`: Extract PMI-based lexical keywords.
*   `12_feature_pcfg_builder.ipynb`: Construct PCFG syntactic vectors.
*   `13_feature_prag_vectors.ipynb`: Build pragmatic style centroids.
*   `14_feature_rag_index.ipynb`: Build FAISS indexes for RAG retrieval.

### 3: Model Training (Core)
*   **Main**: `22_train_sft_main.ipynb` (Train the Qwen-based Style-SFT model).
*   **Baselines**: `23_train_sft_vanilla.ipynb`, `24_train_sft_per_char.ipynb`.
*   **Evaluator**: `21_train_style_classifier.ipynb` (Train the RoBERTa style classifier).

### 4: Evaluation & Analysis (Required for main results)
*   `31_eval_gen_neutral.ipynb`: Generate datasets for evaluation.
*   `32_eval_collect_outputs.ipynb`: Batch inference and collection.
*   `33_eval_automated.ipynb`: Run automated evaluation metrics.
*   `34_eval_significance.ipynb`: Statistical significance testing.
*   `35_ana_syntactic_dim.ipynb`: Analyse syntactic dimensions.
*   `36_ana_style_extract_frieren.ipynb`: Case study (Frieren).

## Minimal Reproducion

To reproduce the main quantitative results (Table 5-1, Figure 5.1):

1. Set up the environment (see Environmental Setup)
2. Download preprocessed data and pretrained evaluators (see Outputs & Models)
3. Run the following notebooks in order:
   - 31_eval_gen_neutral.ipynb
   - 32_eval_collect_outputs.ipynb
   - 33_eval_automated.ipynb
   - 34_eval_significance.ipynb

## Notes on Randomness

All experiments use fixed random seeds where applicable.
Minor numerical differences may occur due to GPU nondeterminism,
but relative rankings and statistical conclusions should remain stable.

## External Dependencies & Configuration

Some baselines and data generation steps require access to external APIs (e.g., HanLP for parsing, OpenAI/GLM for neutral sentence generation).

Please create a `.env` file in the root directory `OtakuLab/` with the following keys:

```ini
# API Keys for Data Generation & Baselines
OPENAI_API_KEY="sk-..."       # Compatible with OpenAI SDK (e.g., DeepSeek, Qwen)
OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
OPENAI_CHAT_MODEL="glm-4"     # Model name to use for generation (e.g., glm-4, qwen-turbo)
HANLP_API_KEY="..."           # HanLP Auth Key for PCFG parsing
```

> **Note**: HanLP is used for constructing syntactic vectors (PCFG). You can obtain a key from [HanLP](https://hanlp.hankcs.com/).

## Data Usage Notice

All datasets are used strictly for academic research.
Character dialogues are extracted from publicly available fan-transcribed sources.
No original copyrighted material is redistributed in raw form.
