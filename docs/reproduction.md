# Reproduction guide

[Project overview](../README.md) · [Repository map](repository-map.md) · [Output inventory](../outputs/README.md)

## Reproduction levels

| Level | Establishes | Current status |
| --- | --- | --- |
| Inspect saved results | Understand supplied samples and scores | Available without model downloads |
| Re-run statistics | Test supplied paired arrays | Available with NumPy/SciPy; confirm pairing |
| Re-score generations | Recompute style and semantic scores | Needs trained classifier and base models |
| Re-run inference | Generate new responses | Needs generator and baseline resources |
| Re-train from data | Rebuild features and models | Needs external inputs, path alignment, validated environment |

The first two levels have their core inputs in tracked files. This documentation audit ran the saved-result example and notebook 34's code. It did not validate training, inference, or API services.

The latest training and evaluation inputs are published on `v2`; see the [data snapshot](../data/README.md). These additions were made during double-blind review, which has ended. The paper's data will be updated later. Paper and review-period expanded results are both published as distinct snapshots; see [experiment provenance](experiment-provenance.md).

## Inspect saved results

From the repository root, run this read-only Python example:

```python
import json
from pathlib import Path

with Path("outputs/evaluate_result.jsonl").open(encoding="utf-8") as stream:
    metrics = json.load(stream)  # One JSON object, despite the .jsonl suffix.

for model, values in metrics.items():
    semantic = values["semantic"]
    style = values["style"]
    valid_style = values["valid_style"]
    assert len(semantic) == len(style) == len(valid_style)
    print(model, "samples:", len(semantic))
    print("semantic:", sum(semantic) / len(semantic))
    print("stored VSS:", sum(valid_style) / len(valid_style))
```

This summarizes stored scores. The tracked and local metric arrays were checked against the confirmed 0.1 penalty. Main-system aggregates were compared with the local paper table. Pairing is checked against the matched generation snapshot and per-character arrays; notebook 34 aligns sample keys before testing.

Tracked generations contain 6,000 rows: 150 neutral sentences × eight characters × five systems. At the audited HEAD, the metric object includes a sixth ablation system, with 1,200 entries per system. `outputs/evaluate_result_extra.jsonl` contains five systems with 1,840 entries each. These metrics are an expanded snapshot, not replacements for the paper main table.

For statistics, open [notebook 34](../notebooks/34_eval_significance.ipynb). It compares `Ours(DPO)` against `BaselineA`, `BaselineB`, and `BaselineC` for semantic and valid-style scores. It uses two-sided Wilcoxon tests with Bonferroni correction across six comparisons.

Equal array lengths do not establish pairing. Every index must describe the same sentence and character across systems.

## Environment and configuration

Use the commands in [README](../README.md#environment-preparation). The dependency file is not a frozen paper environment. Check Transformers and TRL compatibility together.

During this audit, the global Conda Python imported a user-installed NumPy 2 package alongside an incompatible SciPy binary. The statistics check passed with `python -s`, which excludes user-site packages. Use a dedicated environment and kernel; this workaround is not a validated environment specification.

Notebook imports directly use `hanlp_restful`, `hanlp_common`, `datasets`, and `tiktoken`. The supplemental install command covers these and the interface. Package references: [HanLP REST](https://pypi.org/project/hanlp-restful/), [HanLP common](https://pypi.org/project/hanlp-common/), [Datasets](https://pypi.org/project/datasets/), [tiktoken](https://pypi.org/project/tiktoken/), [JupyterLab](https://pypi.org/project/jupyterlab/).

Training uses BF16 in selected model loads and machine-specific CUDA paths. The read-only example supports CPU inspection. CPU fallback code does not establish CPU training support. No tested GPU memory minimum is documented.

`requirements.txt` includes `flash-attn` on non-Windows systems. Check the matching PyTorch/CUDA build. Main SFT explicitly uses SDPA; confirm whether your route needs FlashAttention. See [upstream installation requirements](https://github.com/Dao-AILab/flash-attention#installation-and-features). `faiss-cpu` is listed; notebook 14 builds a CPU index.

Copy [.env.example](../.env.example) to `.env` for API stages:

| Variable | Use |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI-compatible clients |
| `OPENAI_BASE_URL` | Selected provider endpoint |
| `OPENAI_CHAT_MODEL` | Most generation and judge sections |
| `BASELINE_C_MODEL` | Notebook 32 Baseline C; default `glm-4.7` |
| `NEUTRAL_MODEL` | Notebook 31's neutral generation |
| `HANLP_API_KEY` | HanLP REST tokenization and constituency parsing |

Choose provider and model together. A single model setting may not suit generation, Baseline C, and judging. Record the effective model separately for each stage. API calls may incur charges.

Most cells expect the repository root. Check the kernel:

```python
from pathlib import Path
print(Path.cwd())
print((Path.cwd() / "data").is_dir())
```

Notebooks 21, 32–34, and 36 locate the repository root from their kernel directory. Notebook 32 accepts `QWEN_MODEL_PATH`, `SFT_CHECKPOINT`, `DPO_CHECKPOINT`, and `VANILLA_CHECKPOINT`; defaults use `../Models` and `outputs/model`. Align remaining `/root/autodl-tmp`, `../Models`, and `../Dataset` resources in other sections. Notebook 24 changes directories unconditionally. Notebook 38 expects a kernel in `notebooks/`; from the repository root, set `OTAKU_ROOT = Path.cwd()`. Notebook 15 searches for a parent containing both `OtakuLab/` and `Models/`.

## Evaluate existing generations

1. Select a fixed test set and matching generations.
2. Obtain the RoBERTa backbone, classifier checkpoint, label encoder, and BGE model.
3. In notebook 33, align `BATCH_INFERENCE_FILE`, `NEUTRAL_EVAL_FILE`, `BACKBONE_PATH`, `CHECKPOINT_PATH`, and semantic `MODEL_PATH`.
4. Use the paper-standard 0.1 VSS penalty below or at the semantic threshold. Keep `USE_HELD_OUT=False` for the paper training-split centroids. A missing held-out export stops the optional sensitivity route.
5. Run scoring sections. Outputs and figures use the selected route directory; supplied snapshots are preserved.
6. Use the same route in notebook 34. It validates and aligns sample keys before testing.

API judging is an additional section. It is not required to inspect saved classifier/semantic arrays.

### Shared evaluation route

Set `EVALUATION_VARIANT = "paper"` or `"expanded"` in notebooks 32, 33, and 34. All three must use the same selection.

| Route | Test set | Saved generations | Saved metrics |
| --- | --- | --- | --- |
| `paper` (default) | `data/neutral_sentences_eval.jsonl` | `outputs/batch_run_result.jsonl` | `outputs/evaluate_result.jsonl` |
| `expanded` | `data/neutral_sentences_eval_extra.jsonl` | `outputs/batch_run_result_extra.jsonl` | `outputs/evaluate_result_extra.jsonl` |

New generation, metric, figure, and API judge files go to `outputs/runs/<route>/`. Notebook 33 uses the current run's generations when present; otherwise it reads the saved snapshot. It prints the chosen source. Notebook 34 uses the generation file bound to the chosen metric file. A partly generated run cannot replace the input to saved-result statistics.

Notebook 32 replaces complete system groups during export; reruns cannot append duplicate pairs. A generation with an error marker stops evaluation. New metrics include sample IDs and hash manifests. Notebook 34 stops if their generation, test, or metric files changed after scoring.

Notebook 31 creates a new test set and can overwrite the supplied base input. Skip it when reproducing either saved snapshot.

Run the lightweight integrity tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

### Metric definitions

Notebook 33 computes semantic cosine similarity from normalized BGE embeddings. Style scores come from the classifier. H-Score is their harmonic mean with a small denominator constant.

The maintainer confirmed that the reported experimental data use the following definition. Use it for paper reproduction:

```text
VSS = style_score × (1 if semantic_score > 0.75 else 0.1)
```

At a semantic score of exactly 0.75, the multiplier is 0.1. Notebooks 33 and 38 and the stored main metric arrays follow this rule. No recalculation is needed to adopt this standard.

Local recalculation scripts implement a separate hard-gate sensitivity analysis:

```text
VSS = style_score × (1 if semantic_score > 0.75 else 0)
```

The hard-gate definition is not the reported experimental metric. Keep those comparison outputs separate from the main result file. Use the 0.1 definition for the main metrics, significance tests, and figures. Record the formula in experiment manifests.

`recompute_vss_150.py` takes only the first 150 metric entries per system. The main experiment has 1,200 sentence-character pairs per system. This slice does not recover the full 150-sentence experiment.

## Train and generate

After aligning paths, use these routes for supplied processed data:

1. Run notebook 22's data sections only when rebuilding training exports. Preserve supplied snapshots by skipping re-export.
2. Train the evaluator with 21. It depends on 22's data export. Keep `CLASSIFIER_SCOPE="paper"` for eight roles. The optional Frieren classifier uses a different directory; held-out export defaults off.
3. Train SFT with 22. Keep `lora/`, `style_encoder.pt`, and `tokenizer/` together.
4. Build pairs with 16, then format and train DPO with 24. Align pair filenames and SFT checkpoint. Notebook 24 replaces the rejected `<think>` block with the chosen block.
5. Build Baseline A retrieval resources with 14. Notebook 23 exports vanilla data; train the baseline separately. Notebook 32 defaults to `outputs/evaluate/baseline/Vanilla`; override `VANILLA_CHECKPOINT` for an external adapter.
6. Use the supplied test set. Run 31 only when intentionally creating a different set.
7. Align artifacts and test inputs in 32. Generate responses, then follow the evaluation route above.

To rebuild upstream data, run selected sections of 01 and 02 for cleaning and neutral sentences. Build features with 11/12/13, then return to 02's CoT sections. These stages need external corpora and APIs.

Notebook 12 currently exports `style_vector_phase2_robust_bounded.json`, while notebooks 02, 22, and 23 read the tracked `style_vector_phase2_minmax.json`. These represent different normalization choices. Select the intended feature version and update consumers together; renaming alone does not establish equivalent values.

### Model resources

| Resource | Required role or files | Availability |
| --- | --- | --- |
| Qwen3-1.7B | Generator backbone, config, tokenizer | Upstream model; configure local path |
| `chinese-roberta-wwm-ext` | Classifier backbone | Upstream model; configure local path |
| `bge-large-zh-v1.5` | Semantic scoring, filtering, pragmatic embedding | Upstream model; configure local path |
| SFT | `lora/`, `style_encoder.pt`, `tokenizer/` | No documented public release |
| DPO | Adapter plus required SFT style encoder | No documented public release |
| Classifier | Checkpoint, `label_encoder.json`, optional held-out files | No documented public release |
| RAG | FAISS indexes and matching role corpora | Not tracked; build with 14 |
| DPO pairs | Raw pairs; formatted `prompt`, `chosen`, `rejected` JSONL | Included under `data/dpo_train/`; align older notebook defaults |

Notebook 22 saves v4.3 with a learning-rate suffix, but its inference section loads v5.0. Other cells load v4.3 with different suffixes or DPO checkpoints. Set consumers to the artifacts you produced.

## Record an experiment

Record the Git revision and local diff, paper version, file hashes, sample counts, characters, model revisions, checkpoints, metric formula, thresholds, seeds, package versions, and hardware. Preserve generation settings and API model identifiers.

Several cells use seed 42. This does not make the workflow deterministic. Sampling, API revisions, GPU kernels, and environment changes can affect results. Stable rankings need revalidation.
