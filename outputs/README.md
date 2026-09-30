# Output inventory

[Project overview](../README.md) · [Reproduction guide](../docs/reproduction.md) · [Experiment provenance](../docs/experiment-provenance.md)

Updated on 2026-09-30. File hashes and counts are recorded in [evaluation-snapshots.json](evaluation-snapshots.json).

## Published evaluation snapshots

| File | Contents |
| --- | --- |
| `batch_run_result.jsonl` | Historical paper generations: 150 sentences × 8 characters × 5 systems = 6,000 rows |
| `evaluate_result.jsonl` | Historical paper metrics: 1,200 entries per system; includes an additional ablation array |
| `batch_run_result_extra.jsonl` | Review-period expanded generations: 230 × 8 × 5 = 9,200 rows |
| `evaluate_result_extra.jsonl` | Expanded metrics: 1,840 entries per system, 5 systems |
| `llm_eval_batch_output.jsonl` | Historical batch judge responses: 6,000 rows; separate from expanded metrics |

Both metric files contain **one JSON object**, despite their historical `.jsonl` suffix. Use `json.load`. Main VSS arrays use `style × (1 if semantic > 0.75 else 0.1)`.

The expanded results are pending a paper update. Their original Ours responses were regenerated; they are not a simple extension of the old output file. See the provenance audit for confirmed checkpoint directories and missing historical run metadata.

Notebooks 32–34 write new runs under `runs/paper/` or `runs/expanded/`. These directories are ignored. They contain separate generations, metrics, figures, API judge files, and hash manifests. Published snapshots remain unchanged.

## Published features

| Path | Contents |
| --- | --- |
| `style/signature/lexical/*_pmi_filtered.json` | Lexical keywords |
| `style/signature/punctuation/` | Punctuation and formatting signatures |
| `style/dense/raw/`, `style/dense/normalized/` | Structural features |
| Selected `style/dense/diagnostics/` files | Dialogue-act diagnostics |
| `style/semantic/prag_vectors/*.jsonl` | Pragmatic labels and scores |
| `style/semantic/prag_vectors/frieren.jsonl` | Historical 25-sample Frieren pragmatics |
| `style/semantic/prag_vectors/frieren_80.jsonl` | Review-period 80-sample pragmatics; original 25-row prefix unchanged |
| `meta_learner/*.pth` | Three small checkpoints |

## Model resources and local artifacts

Classifier checkpoints, generator adapters, Baseline B adapters, and RAG indexes remain local resources. No public download is documented. Train with notebooks 21/22/24, build RAG with 14, and configure the Vanilla adapter separately. DPO datasets are published under `data/dpo_train/`.

The main classifier uses `evaluate/style-classifier/`. The optional nine-role extension uses `evaluate/style-classifier-frieren/`. Model directories are ignored. The three tracked meta-learner checkpoints remain tracked despite their ignore pattern; notebook 13 also refers to `style/models/meta_learner/`.

Local curation inputs, review files, trial requests, and hard-gate comparisons are retained and ignored. Their producer and consumer references are recorded in [local-artifacts.md](../docs/local-artifacts.md).
