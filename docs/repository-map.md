# Repository map

[Project overview](../README.md) · [Reproduction guide](reproduction.md) · [发布前检查](release-readiness.md)

Checked on 2026-09-30 against tracked paths at `dc1feae` and the working tree. Counts describe that snapshot, not a release manifest.

The subsequent `v2` data publication uses the latest local state after double-blind review. See the [data snapshot](../data/README.md) and [manifest](../data/manifest.json) for the current dataset inventory. Historical outputs and uncommitted notebook changes remain separate.

## Directory responsibilities

| Path | Responsibility | Availability |
| --- | --- | --- |
| `data/` | Corpora, neutral sentences, training exports, test inputs | Latest canonical files included, with DPO datasets and expanded evaluation input |
| `notebooks/` | Experiment definitions | 20 tracked notebooks; four locally modified |
| `outputs/style/signature/` | Lexical PMI and punctuation signatures | Tracked |
| `outputs/style/dense/` | Structural vectors and diagnostics | Selected files tracked; constituency caches ignored |
| `outputs/style/semantic/prag_vectors/` | Character pragmatic labels/scores | Tracked |
| `outputs/meta_learner/` | Three small PyTorch checkpoints | Already tracked, despite current ignore rule |
| `outputs/evaluate/` | Classifier, baselines, and RAG resources | Ignored; not supplied by tracked files |
| `outputs/model/` | Generator artifacts used by some cells | Ignored; no documented public download |
| `scripts/` | Local curation and VSS recalculation | Untracked at audit; includes absolute Windows paths |
| `LaTex/` | Generated paper figures | Ignored; no tracked paper source |

Ignoring a directory does not remove files already tracked. Check `git ls-files`, not directory existence.

## Notebook catalog

Numbers group stages. Several notebooks contain historical and current sections. Follow the dependencies in the [reproduction guide](reproduction.md).

| Notebook | Actual responsibility | Main dependencies or limitations |
| --- | --- | --- |
| [01_dataset_clean](../notebooks/01_dataset_clean.ipynb) | Clean Haruhi; extract/filter Wukong dialogue | External sources; optional API translation/filtering |
| [02_dataset_gen_neutral_train](../notebooks/02_dataset_gen_neutral_train.ipynb) | Generate neutral training sentences and CoT | External Muice data; API; CoT section needs style features |
| [11_feature_pmi_builder](../notebooks/11_feature_pmi_builder.ipynb) | Tokenize corpora and extract PMI keywords | HanLP REST API; legacy and v2 sections |
| [12_feature_style_vector_phase2](../notebooks/12_feature_style_vector_phase2.ipynb) | Extract punctuation and structural features | HanLP; normalization excludes Frieren holdout |
| [13_feature_prag_vectors](../notebooks/13_feature_prag_vectors.ipynb) | Train meta-learners; infer pragmatic labels | BGE; annotated data; mixed checkpoint paths |
| [14_feature_rag_index](../notebooks/14_feature_rag_index.ipynb) | Build baseline retrieval indexes | Training export; embedding model; FAISS |
| [15_nshot_stability](../notebooks/15_nshot_stability.ipynb) | Measure Muice style-vector stability | RAG corpus; features; sibling `OtakuLab/` and `Models/` |
| [16_build_dpo_pairs](../notebooks/16_build_dpo_pairs.ipynb) | Construct preference pairs | SFT checkpoint; Qwen3; ablation-named output file |
| [19_feature_pcfg_builder(deprecated)](../notebooks/19_feature_pcfg_builder%28deprecated%29.ipynb) | Historical PCFG extraction | Deprecated; not the current structural-feature entry |
| [21_train_style_classifier](../notebooks/21_train_style_classifier.ipynb) | Train classifier and export held-out embeddings | Notebook 22's oversampled data export; RoBERTa |
| [22_train_sft_main](../notebooks/22_train_sft_main.ipynb) | Build training files; train, export, and load SFT | CoT; features; Qwen3; BGE filtering; different save/load versions |
| [23_train_sft_vanilla](../notebooks/23_train_sft_vanilla.ipynb) | Export baseline conversations | Data preparation only; no executable training stage |
| [24_train_dpo_main](../notebooks/24_train_dpo_main.ipynb) | Format CoT-shared pairs; train/export DPO | Pair data; SFT LoRA; TRL; hard-coded remote root |
| [31_eval_gen_neutral](../notebooks/31_eval_gen_neutral.ipynb) | Generate neutral evaluation sentences | External Haruhi path; API; skip for the supplied fixed test set |
| [32_eval_collect_outputs](../notebooks/32_eval_collect_outputs.ipynb) | Generate model and baseline responses | Weights; RAG; Baseline C API; local default uses extra test set |
| [33_eval_automated](../notebooks/33_eval_automated.ipynb) | Detect degeneration, score, plot, and judge | Classifier; RoBERTa; BGE; optional API; extra generations locally |
| [34_eval_significance](../notebooks/34_eval_significance.ipynb) | Paired Wilcoxon tests with Bonferroni correction | Score arrays with matching sample order |
| [35_ana_syntactic_dim](../notebooks/35_ana_syntactic_dim.ipynb) | Historical 10-D/18-D comparison | Old `dataset/`, `evaluate/outputs/`, and five-role paths |
| [36_ana_style_extract_frieren](../notebooks/36_ana_style_extract_frieren.ipynb) | Extract held-out style and evaluate rewrites | Frieren data; features; meta-learner; generator and classifier |
| [38_ablation_style_vectors](../notebooks/38_ablation_style_vectors.ipynb) | Ablate feature layers and CoT | Model; evaluator; assumes working directory is `notebooks/` |

## Data formats

JSON files hold one complete array or object. JSONL normally holds one object per line. See the [output inventory](../outputs/README.md) for a legacy exception.

| File | Main fields | Tracked snapshot |
| --- | --- | --- |
| `data/neutral_sentences.jsonl` | `character`, `original`, `neutral` | 10,965 rows |
| `data/neutral_sentences_with_CoT.jsonl` | Above fields plus `CoT` | 10,921 rows |
| `data/llm_train.json` | `character`, `neutral_sentence`, `instruction_components`, `thinking_process`, `output` | 8,272 rows |
| `data/llm_train_oversampling.json` | Same schema, with oversampling | 9,521 rows |
| `data/vanilla_llm_train.json` | `conversations`, `system` | 10,179 rows |
| `data/golden_annotation.jsonl` | `user_prompt`, `agent_response`, `tags` | 731 rows |
| `data/neutral_sentences_eval.jsonl` | `subset`, `neutral` | 150 rows |
| `data/frieren.jsonl` | `character`, `context`, `original`, `neutral` | 80 in current snapshot; 25 at audit baseline |
| `data/neutral_sentences_eval_extra.jsonl` | `subset`, `neutral` | 230 rows, including the original 150-row prefix |
| `data/raw/Haruhi/Haruhi_clean.jsonl` | Dialogue fields including `agent_role`, `agent_response` | 9,272 rows |
| `data/raw/wukong/wukong_dialog_qa.jsonl` | `user_question`, `agent_response` | 700 rows |
| Wukong `*_preclean.jsonl` and `*_audit.jsonl` | Candidate pairs; audit adds filtering decisions | 1,507 rows each |

`data/raw/` contains processed exports. Original upstream corpora are not all included. Other inputs use external paths such as `../Dataset/Muice/` and `../Dataset/PsyDTCorpus/`.

## Main data flow

```text
Source corpora -> 01 cleaning -> 02 neutral-sentence section
Source corpora -> 11 / 12 / 13 -> style features
Neutral sentences + features -> 02 CoT section -> 22 data export
22 data export -> 21 style classifier
22 data export -> 22 SFT -> 16 preference pairs -> 24 DPO
22 data export -> 14 retrieval index
CoT data + features -> 23 vanilla export -> external baseline training
Fixed test set + model resources -> 32 generations -> 33 scores -> 34 tests
```

Notebook 16's output does not match notebook 24's default input. Baseline training used by notebook 32 is not supplied as a complete notebook procedure.

## Local helpers

These scripts support local experiments; they are not a stable command-line interface.

| Group | Files | Behavior to check |
| --- | --- | --- |
| Subtitle extraction | `extract_ass_dialogue.py` | Reads a local `D:` directory and writes dialogue output |
| Frieren review | `build_candidates.py`, `build_candidates_v2.py`, `curate_v3.py`, `make_review_file.py`, `build_final_review.py` | Writes review text to absolute paths |
| Frieren row preparation | `build_final_entries.py` | Reads existing data and writes proposed additions |
| Test-set expansion | `expand_neutral_eval_lccc.py`, `neutralize_lccc_sentences.py` | Can modify the fixed test set; both expose `--dry-run` |
| VSS sensitivity analysis | `recompute_vss.py`, `recompute_vss_150.py`, `full_vss_pipeline.py` | Hard-gate comparison only; main paper metric uses 0.1; absolute paths; 150-row slicing is not the full test set |

Keep curated additions and test variants separate until their provenance and intended experiment are recorded.
