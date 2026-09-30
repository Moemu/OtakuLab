# 本地文件引用核对

[实验来源](experiment-provenance.md) · [仓库地图](repository-map.md)

核对覆盖 Notebook 的代码单元、脚本、文档和上级论文源码。执行输出中的旧路径不视为代码依赖。动态拼接、外部命令和手工使用可能不出现字面引用，因此本次保留全部本地文件。

## 纳入发布的有效结果

| 文件 | 引用及处理 |
| --- | --- |
| `outputs/batch_run_result_extra.jsonl` | 33 号扩展评估输入；纳入结果快照 |
| 本地修改版 `outputs/evaluate_result.jsonl` | 已原样存为 `evaluate_result_extra.jsonl`；历史基础文件恢复 |
| `outputs/pragmatic/frieren.jsonl` | 原为 36 号的生产者和消费者路径；80 条内容已复制到 `outputs/style/semantic/prag_vectors/frieren_80.jsonl`；36 号新运行使用独立目录 |
| `scripts/evaluation_io.py` | 新增的主评估路径、覆盖检查、导出及配对工具；32、33、34 号直接引用 |

## 已纳入数据的备份和补充文件

| 文件 | 核对结果 |
| --- | --- |
| `data/frieren_backup_25.jsonl` | 没有代码字面引用；与当前 80 条数据的前 25 条一致 |
| `data/frieren_new_entries.jsonl` | `build_final_entries.py` 的输出；55 条已逐条纳入 `data/frieren.jsonl` |

这两份文件保留在本地并忽略。主 Notebook 读取规范数据文件。

## 仍有本地整理用途的文件

| 文件或脚本 | 引用关系 |
| --- | --- |
| `outputs/all_dialogue.jsonl` | `extract_ass_dialogue.py` 写入；多个候选筛选和审阅脚本读取 |
| `outputs/frieren_candidates_review.txt` | `build_candidates.py`、`build_candidates_v2.py` 输出 |
| `outputs/frieren_candidates_v3.txt` | `curate_v3.py` 输出 |
| `outputs/frieren_candidates_FINAL.txt` | `build_final_review.py` 输出 |
| `scripts/extract_ass_dialogue.py` | 从本地字幕提取对白；存在本机目录 |
| `scripts/build_candidates.py`、`build_candidates_v2.py`、`curate_v3.py` | 本地候选筛选 |
| `scripts/build_final_entries.py`、`build_final_review.py`、`make_review_file.py` | 补充样本和人工审阅文件生成 |
| `scripts/expand_neutral_eval_lccc.py`、`neutralize_lccc_sentences.py` | 评估集补充试验；主 Notebook 不调用；部分写入基础评估文件，不能直接当作当前复现入口 |

这些文件构成本地数据整理链路，不能因主 Notebook 未调用而删除。保留并加入精确忽略规则，避免把试验脚本当作稳定接口发布。

## 对照分析和没有找到代码引用的文件

| 文件 | 核对结果及处理 |
| --- | --- |
| `scripts/recompute_vss.py`、`full_vss_pipeline.py`、`recompute_vss_150.py` | 乘 0 的硬门控对照；不是论文主指标；保留在本地 |
| `outputs/evaluate_result_vss_hard.jsonl` | `recompute_vss.py` 的输出；保留为对照 |
| `outputs/baseline_c_batch_input.jsonl` | 未找到消费者；1,840 条试验请求使用 `glm-4.5-air`；与扩展回答的关系未证实 |
| `outputs/ep12_28_dialogue.txt`、`frieren_context.txt`、`frieren_mentions.jsonl` | 未找到代码字面引用；保留为本地中间资料 |
| `outputs/frieren_candidates_review_v2.txt` | 未找到代码字面引用；保留为本地审阅资料 |

本次没有删除上述文件。后续若要删除，应再核对人工整理用途和外部引用。
