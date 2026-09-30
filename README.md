# OtakuLab

[English](README.md) | [简体中文](README.zh-CN.md)

OtakuLab contains the experiments for **Structured Style-Rewrite with Chain-of-Thought Planning for Low-Resource Character Dialogue**.

[Paper (arXiv:2603.05933)](https://arxiv.org/abs/2603.05933) · [Paper v2](https://arxiv.org/abs/2603.05933v2) · [Repository](https://github.com/Moemu/OtakuLab)

The task is sentence-level rewriting: preserve a neutral sentence's meaning while expressing a target character's style. The framework combines formatting signatures, structural features, pragmatic traits, and chain-of-thought (CoT) planning. Training uses supervised fine-tuning (SFT), followed by CoT-shared direct preference optimization (DPO).

The main training workflow covers eight characters: Muice, Ayaka, Zhongli, Hu Tao, Haruhi, Li Yunlong, Sheldon, and Wukong. Frieren is a separate held-out character study. Historical experiments also reference PsyDC and other roles.

## Current availability

This is a notebook-based research repository. The `v2` branch includes the latest local training data, DPO datasets, the expanded 230-sentence evaluation set, and 80 Frieren samples. It also includes style features, historical saved generations and evaluation arrays, and three small meta-learner checkpoints. See the [data snapshot](data/README.md) and its file hashes.

The additions were prepared during double-blind review. That review period has ended. The maintainer will update the paper's experimental data later; this repository snapshot does not claim that the current paper already reports the expanded data.

**A fresh clone does not yet provide a complete, verified training or inference run.** Generator adapters, the trained style classifier, and RAG indexes have no documented public download location. Notebooks also contain machine-specific paths and different experiment versions. Read the [reproduction guide](docs/reproduction.md) before running cells.

The reported experiments use VSS = style score × (1 if semantic score > 0.75 else 0.1). This is the reproduction standard, confirmed by the maintainer. Hard-gated recalculation scripts are separate sensitivity analyses. Notebooks 32–34 share paper/expanded routes; record the Git revision and test set when comparing results.

## Choose a starting point

| Goal | Start here | Additional resources |
| --- | --- | --- |
| Understand the method and files | [Repository map](docs/repository-map.md) | None |
| Inspect saved results | [Saved-result walkthrough](docs/reproduction.md#inspect-saved-results) | Python; no GPU or API key |
| Score existing generations | [Evaluation route](docs/reproduction.md#evaluate-existing-generations) | Classifier checkpoint, RoBERTa, BGE |
| Train and generate outputs | [Training route](docs/reproduction.md#train-and-generate) | Base models, training hardware, selected external data |
| Prepare a wider release | [发布前检查](docs/release-readiness.md) | Maintainer decisions and validation |

## Repository layout

```text
OtakuLab/
├── data/                 # Processed corpora, training sets, evaluation inputs
├── notebooks/            # Feature, training, evaluation, and analysis notebooks
├── outputs/              # Tracked results/features and local model artifacts
├── scripts/              # Local curation and metric-recalculation helpers
├── docs/                 # Repository map, reproduction guide, release checks
├── LaTex/                # Local figure outputs; ignored by Git
├── .env.example          # API configuration template; no credentials
├── requirements.txt      # Research dependencies; not a version lock
├── CONTRIBUTING.md       # Contribution and experiment-reporting guidance
└── CITATION.cff          # Paper citation metadata
```

`scripts/evaluation_io.py` provides shared evaluation paths and integrity checks. Local curation scripts remain ignored; see the [artifact audit](docs/local-artifacts.md).

Saved paper and expanded results are published separately. Notebooks 32–34 default to the paper route and write new runs under `outputs/runs/`. See [experiment provenance](docs/experiment-provenance.md).

## Environment preparation

The previous setup used Python 3.12 and Conda. This is a starting point, not a validated compatibility matrix.

```bash
git clone --branch v2 https://github.com/Moemu/OtakuLab.git
cd OtakuLab
conda create -n otakulab python=3.12
conda activate otakulab
python -m pip install -r requirements.txt
python -m pip install jupyterlab hanlp-restful hanlp-common datasets tiktoken
python -m ipykernel install --user --name otakulab --display-name "OtakuLab"
python -m jupyterlab
```

The supplemental command installs the notebook interface and covers imports not listed directly in `requirements.txt`. See [environment notes](docs/reproduction.md#environment-and-configuration) for CUDA and FlashAttention limitations.

Select the `OtakuLab` kernel. Check `Path.cwd()` and input/output constants before execution. Notebook numbers group stages; they do **not** define a single execution order. Most cells expect the repository root, while some analysis notebooks use other root rules.

Copy `.env.example` to `.env` for API-based steps. In PowerShell:

```powershell
Copy-Item .env.example .env
```

Set a matching endpoint, model, and key. API generation and judging may incur charges. Saved-result inspection needs no credentials.

## Data and reuse

The repository contains character dialogue text and derived data. The earlier statement that no copyrighted material was redistributed did not account for these files. Source provenance and redistribution terms need a file-level review.

No repository `LICENSE` file was present during this audit. Code, data, model weights, and upstream sources need explicit reuse terms before a broader release. The paper's license does not define repository licensing.

## Citation

```bibtex
@misc{zhu2026structuredstylerewrite,
  title = {Structured Style-Rewrite with Chain-of-Thought Planning for Low-Resource Character Dialogue},
  author = {Chanhui Zhu},
  year = {2026},
  eprint = {2603.05933},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.2603.05933},
  url = {https://arxiv.org/abs/2603.05933}
}
```

Use the [contribution guide](CONTRIBUTING.md) to report a reproduction issue. Include the Git revision, notebook cells, resource versions, and error details.
