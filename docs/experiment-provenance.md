# 实验版本与来源核对

[复现指南](reproduction.md) · [本地文件引用核对](local-artifacts.md) · [结果清单](../outputs/evaluation-snapshots.json)

核对日期：2026-09-30。数据发布基线为 `e7f8a39`。Git 历史不能单独证明实际采用的实验版本。

## 论文结果和评审期扩展

| 项目 | 论文历史结果 | 评审期扩展结果 |
| --- | --- | --- |
| 评估集 | `neutral_sentences_eval.jsonl`，150 句 | `neutral_sentences_eval_extra.jsonl`，230 句 |
| 角色 | 8 个主实验角色 | 相同 8 个角色 |
| 生成文件 | `batch_run_result.jsonl`，6,000 条 | `batch_run_result_extra.jsonl`，9,200 条 |
| 指标文件 | `evaluate_result.jsonl`，主实验每系统 1,200 项 | `evaluate_result_extra.jsonl`，每系统 1,840 项 |
| Ours(SFT) VSS | 0.609565 | 0.602671 |
| Ours(DPO) VSS | 0.631949 | 0.607935 |
| 与论文的关系 | 主表对应的历史快照 | 后续回填论文的数据，当前单独标记 |

两个指标文件均为单个 JSON 对象。历史指标还包含 `DPO(wo/CoT_Shared)` 消融数组；当前主生成文件只覆盖 5 个系统。主统计链路不推断缺失的消融生成结果。

历史指标文件已恢复为 `e7f8a39` 中的原始字节。本地修改版已原样保存为 `evaluate_result_extra.jsonl`。本次没有重新生成回答或重算模型评分。文件哈希见结果清单。

扩展结果包含原有的全部句子和角色组合。三个 Baseline 的原 1,200 条回答与指标保持不变。两个 Ours 系统的原有回答也重新生成过，不能把扩展结果视为只追加 80 句。去除思考段后，仅 21 条 SFT 和 29 条 DPO 回答与历史版本相同。

## 论文源码证据

本地依据是上级目录的 `LaTex/main.tex`、`LaTex/sections/experiments.tex` 和 `LaTex/sections/appendixes.tex`。也对照了 `arXiv/` 副本。这些源码位于仓库外，不是克隆依赖。

- 实验主表报告 SFT VSS 约 0.610、DPO VSS 约 0.632，与历史数组一致。
- 附录规定主分类器采用 8 类、80/20 分层划分。质心仅由分类器训练集产生，验证集不参与。
- 附录指定 DPO step 150，`beta=0.1`、学习率 `5e-7`，采用共享 CoT。
- Baseline C 使用 GLM-4.7、2-shot、`temperature=0.2`、`top_p=0.95`。
- 芙莉莲部分为 25 条样本的定性分析。80 条样本和 9 类分类器定量评估属于后续扩展。

论文源码的 VSS 公式仍写成指示函数。维护者已确认，实际论文实验采用：

```text
VSS = style_score × (1 if semantic_score > 0.75 else 0.1)
```

历史和扩展数组都已逐项核对。语义分恰好为 0.75 时乘 0.1。源码公式的修订留待论文回填。

主表部分语义分的末位与原始数组常规四舍五入有小差异。保留原始数组，不为匹配排版数值而修改实验数据。

## Checkpoint 和尚缺的记录

维护者确认扩展 Ours 结果使用以下模型目录：

```text
outputs/model/styled-qwen-v4.3-4e-05
outputs/model/styled-qwen-dpo-v1
```

Notebook 32 的 SFT 和 DPO style encoder 默认指向第一个目录。DPO adapter 默认指向第二个目录下的 `checkpoint-150`，依据论文附录及现有推理代码。

这项确认给出了模型目录。扩展结果没有随文件保存当时的权重哈希、DPO 具体子目录、分类器哈希或质心来源。因此，当前本地权重不能充当历史运行的完整证明。

扩展 Baseline C 新增 80 句的实际 API 模型标识仍待核实。本地试验请求文件使用 `glm-4.5-air`，但未发现它与已保存回答之间的任务 ID 绑定。该试验文件不能证明扩展回答的来源。图表使用通用的 Baseline C 标签。

SFT 附录写学习率 `3e-5`，v4.3 目录名及训练日志出现 `4e-5`。Notebook 22 还有保存 v4.3、加载 v5.0 的历史差异。训练版本核对是后续事项，本次不据目录名改写论文训练参数。

## 评估链路调整

32、33、34 号 Notebook 使用同一项配置：

```python
EVALUATION_VARIANT = "paper"  # 或 "expanded"
```

新运行写入 `outputs/runs/paper/` 或 `outputs/runs/expanded/`。保存的论文和扩展快照保持独立。32 号按完整系统组替换结果，重复执行导出单元不再追加重复行。API 失败记录会阻止结果进入主评估。

33 号检查输入集合、角色、系统、重复项和指标数量。新指标保存明确的样本 ID。运行清单记录评估集、生成文件、质心和指标哈希。34 号检查生成文件与指标的绑定，再按“角色＋中性句”对齐数组。生成或指标在评分后变化时，统计会停止并要求重新评分。

历史文件没有显式样本 ID。其对应关系依据评分代码的顺序、匹配的生成快照和逐角色数组检查恢复。Baseline A、C 的生成顺序与 Ours 不同，直接按原数组下标检验会产生错误配对。新统计会对齐这些顺序，且不修改历史文件。

21 号默认训练 8 类分类器；`CLASSIFIER_SCOPE="frieren"` 使用独立的 `style-classifier-frieren` 目录。held-out 导出和 33 号 `USE_HELD_OUT` 默认关闭。held-out 结果只用于明确选择的敏感性分析。

36 号默认取最新芙莉莲数据的前 25 条。这 25 条已与旧备份逐条核对一致。80 条扩展可显式选择。语用预测写入运行目录；定量评估默认关闭，开启时要求独立的 9 类分类器。旧的 80 条语用预测原样保存为 `style/semantic/prag_vectors/frieren_80.jsonl`。

## 验证范围

本次验证包括两个快照的完整输入覆盖、重复项、指标数量、逐角色顺序和 VSS 公式；5 份 Notebook 的代码语法；评估文件读写与配对保护的单元测试；论文和扩展结果的统计执行。

修改过的 Notebook 已清空旧执行输出，避免回退后残留的 9 类或 held-out 输出造成误读。原始本地 Notebook 已备份在此次整理工作区。

GPU 训练、重新推理和 API 调用未执行。扩展评估器的历史哈希及运行配置仍待补齐。
