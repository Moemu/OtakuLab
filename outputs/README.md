# Output inventory

[Project overview](../README.md) · [Repository map](../docs/repository-map.md) · [Reproduction guide](../docs/reproduction.md)

Checked against `dc1feae` and the working tree on 2026-09-30.

## Tracked artifacts

| Path | Contents | Format |
| --- | --- | --- |
| `style/signature/lexical/*_pmi_filtered.json` | Lexical keywords | JSON |
| `style/signature/punctuation/` | Punctuation and formatting signatures | JSON/CSV |
| `style/dense/raw/`, `style/dense/normalized/` | Structural features | JSON/CSV |
| Selected `style/dense/diagnostics/` files | Dialogue-act diagnostics | JSON |
| `style/semantic/prag_vectors/*.jsonl` | Pragmatic labels/scores | JSONL |
| `meta_learner/*.pth` | Three small checkpoints | PyTorch |
| `batch_run_result.jsonl` | Five-system generations | JSONL; 6,000 tracked rows |
| `evaluate_result.jsonl` | Metric arrays by system | **One JSON object**; use `json.load` |
| `llm_eval_batch_output.jsonl` | Saved batch judge responses | JSONL; 6,000 tracked rows |

The metric file's suffix is historical. Its keys are system names; each system contains metric arrays and may contain `per_char` data. Renaming requires updating consumers.

At the audited HEAD, it contains six systems with 1,200 entries each. The modified local file contains five systems with 1,840 entries each. These describe different snapshots.

The maintainer confirmed that the reported experiments use `style × (1 if semantic > 0.75 else 0.1)`. Both main metric snapshots match that rule. Hard-gated results are sensitivity comparisons and must remain separate.

## Resources absent from tracked files

| Resource | Current path patterns | Recovery route |
| --- | --- | --- |
| Classifier | `evaluate/style-classifier/` | Train with 21; no documented download |
| Generator adapters | `model/`, machine-specific `styled-qwen-*` | Train with 22/24; no documented download |
| Baseline and RAG | `evaluate/baseline/` | Build RAG with 14; baseline training external |
| Token caches | `style/signature/lexical/intermediate_tokens/*.pkl` | Selected sections of 11 |
| Constituency caches | `style/dense/diagnostics/cons/` | Selected sections of 12 |

Some `outputs/styled-qwen-*` paths fall outside ignore patterns. Check new checkpoint paths before staging large files.

Current DPO datasets are included under `data/dpo_train/`. See the [data snapshot](../data/README.md); older notebook defaults still need alignment.

The three `meta_learner/` files remain tracked despite the ignore rule. Notebook 13 also uses `style/models/meta_learner/`. Align locations and checkpoint compatibility.

## Local extensions

At audit time, extra generations, hard-gated metric results, baseline batch input, Frieren review files, and `pragmatic/frieren.jsonl` were untracked. Local presence does not establish GitHub availability.

Current pragmatic features live in `style/semantic/prag_vectors/`. Older `pragmatic/`, `pmi/`, `cons/`, and `rag/` paths appear in historical cells. Check actual tracked files:

```bash
git ls-files outputs
git status --short
git check-ignore -v outputs/evaluate/style-classifier
```

Artifact releases need URLs, sizes, SHA-256 hashes, revisions, label mappings, and reuse terms. The former “upon acceptance” promise had no resource location; this inventory makes no release-date promise.
