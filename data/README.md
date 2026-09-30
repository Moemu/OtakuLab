# Data snapshot

[Project overview](../README.md) · [中文入口](../README.zh-CN.md) · [File manifest](manifest.json)

The `v2` branch publishes the latest local dataset snapshot dated 2026-09-30. Additions were prepared during double-blind review, which has now ended. The maintainer will update the paper's experimental data later. Until that update, use Git revisions and dataset hashes to distinguish this snapshot from published experiments.

## Included data

| File | Rows | Purpose |
| --- | --- | --- |
| `llm_train.json` | 8,272 | Structured SFT training export |
| `llm_train_oversampling.json` | 9,521 | Oversampled SFT export |
| `vanilla_llm_train.json` | 10,179 | Vanilla baseline conversations |
| `neutral_sentences.jsonl` | 10,965 | Neutralized character sentences |
| `neutral_sentences_with_CoT.jsonl` | 10,921 | Sentences with CoT supervision |
| `golden_annotation.jsonl` | 731 | Pragmatic annotations |
| `neutral_sentences_eval.jsonl` | 150 | Original evaluation set |
| `neutral_sentences_eval_extra.jsonl` | 230 | Expanded evaluation set; original 150 rows followed by 80 additions |
| `frieren.jsonl` | 80 | Held-out character samples; previously 25 |
| `dpo_train/dpo_pairs_v43_neutral.json` | 8,272 | Raw preference pairs, JSON array |
| `dpo_train/dpo_pairs_v43_neutral.jsonl` | 8,272 | Raw preference pairs, JSONL |
| `dpo_train/dpo_pairs_wo_cot_shared.jsonl` | 8,272 | Preference-pair input for the no-shared-CoT ablation |
| `dpo_train/dpo_train_v43.jsonl` | 8,220 | Formatted main DPO training data |
| `dpo_train/dpo_train_wo_cot_shared.jsonl` | 8,190 | Formatted no-shared-CoT ablation data |

Processed Haruhi and Wukong exports remain under `raw/`. [manifest.json](manifest.json) lists all 18 included dataset files with row counts, byte sizes, SHA-256 hashes, and fields. Its baseline commit identifies the version before this data publication, not the publication commit itself.

The extra file is an evaluation set. Use the training exports and DPO files for training. Keep the original and expanded evaluation sets separate to preserve comparison with historical results.

Backups and proposed Frieren additions are local curation files. The complete current Frieren dataset is `frieren.jsonl`.

## Experiment alignment

Main VSS uses `style × (1 if semantic > 0.75 else 0.1)`. Select a matching input, generation file, and metric object before comparing runs.

Historical committed generations describe the original 150-sentence test. Publishing the 230-sentence input does not update those generations automatically. Expanded generated outputs and modified notebooks remain local pending a separate results update.

Notebook 24's defaults still use older filenames. For current main training, align its raw pair input with `dpo_train/dpo_pairs_v43_neutral.jsonl` and its formatted dataset with `dpo_train/dpo_train_v43.jsonl`, using paths under `data/`. Keep the no-shared-CoT ablation separate from the main shared-CoT formatter.

Data provenance and reuse terms remain subject to the file-level review described in the project README.
