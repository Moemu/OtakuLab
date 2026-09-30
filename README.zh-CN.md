# OtakuLab

[English](README.md) | [简体中文](README.zh-CN.md)

OtakuLab 服务于论文 [Structured Style-Rewrite with Chain-of-Thought Planning for Low-Resource Character Dialogue](https://arxiv.org/abs/2603.05933) 的实验复现。论文编号为 arXiv:2603.05933，当前公开版本为 [v2](https://arxiv.org/abs/2603.05933v2)。

项目研究句子级角色风格改写。模型保留中性句的含义，再表达目标角色的风格。方法组合格式特征、结构特征、语用特征和思维链（CoT）规划。训练分为监督微调（SFT）和共享 CoT 的直接偏好优化（DPO）。

主训练流程覆盖沐雪、神里绫华、钟离、胡桃、凉宫春日、李云龙、谢尔顿和孙悟空。芙莉莲用于独立的域外角色实验。历史实验还引用 PsyDC 和其他角色。

## 当前能做什么

`v2` 分支包含本地最新训练数据、DPO 数据、230 条扩展评估句和 80 条芙莉莲样本。仓库也包含风格特征、历史生成文本与评估数组，以及 3 份小型元学习器权重。样本数和文件哈希见[数据快照说明](data/README.md)。

**目前还不能承诺从全新克隆直接完成训练或推理。** 生成模型适配器、风格分类器和检索索引缺少公开下载说明。Notebook 还保留本机路径和不同实验版本。运行前请阅读[复现指南](docs/reproduction.md)。详细技术文档使用英文，便于更多研究者阅读。

数据补充发生于双盲评审期间，评审期现已结束。此次按本地最新数据发布，论文中的实验数据后续回填。当前公开论文、仓库数据和历史结果的样本规模可能不同，比较时需记录 Git 版本和评估集。

维护者已确认：论文实验的 VSS 在语义分大于 0.75 时保留风格分，否则将风格分乘 0.1。复现采用此口径，乘 0 的辅助脚本仅用于对照分析。

## 从哪里开始

| 目标 | 文档 | 额外条件 |
| --- | --- | --- |
| 理解目录和 Notebook 职责 | [仓库地图](docs/repository-map.md) | 无 |
| 查看已有实验结果 | [结果检查](docs/reproduction.md#inspect-saved-results) | Python；无需 GPU 或 API 密钥 |
| 对已有生成文本重新评分 | [评估流程](docs/reproduction.md#evaluate-existing-generations) | 分类器权重、RoBERTa 和 BGE |
| 重新训练并生成文本 | [训练流程](docs/reproduction.md#train-and-generate) | 基础模型、训练设备和对应外部数据 |
| 准备公开推广 | [发布前检查](docs/release-readiness.md) | 资源发布、版本核对和运行验证 |

## 目录结构

```text
OtakuLab/
├── data/              # 处理后的语料、训练集和评估输入
├── notebooks/         # 特征提取、训练、评估和分析
├── outputs/           # 已提交的结果、特征，以及本地模型产物
├── scripts/           # 评估路径和完整性检查工具
├── docs/              # 仓库地图、复现指南和发布前检查
├── LaTex/             # 本地图表输出；Git 忽略此目录
├── .env.example       # API 配置模板
├── requirements.txt   # 研究依赖；尚未锁定完整版本
├── CONTRIBUTING.md    # 贡献与实验记录说明
└── CITATION.cff       # 论文引用信息
```

`scripts/evaluation_io.py` 已纳入主评估链路。本地整理脚本保留并忽略，引用核对见[本地文件说明](docs/local-artifacts.md)。

论文结果与评审期扩展结果已分别保存。32～34 号 Notebook 默认使用论文路径，新运行写入 `outputs/runs/`。版本依据见[实验来源核对](docs/experiment-provenance.md)。

## 环境准备

原有配置采用 Python 3.12 和 Conda。以下命令用于准备环境，尚未经过全新环境的完整复现验证。

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

补充安装命令覆盖 Notebook 界面和依赖文件未直接列出的导入项。CUDA、FlashAttention 和版本问题见[环境说明](docs/reproduction.md#environment-and-configuration)。

选择 `OtakuLab` 内核。执行前检查 `Path.cwd()` 和所有输入、输出路径。Notebook 编号表示阶段分组，不能直接视为运行顺序。

需要调用 API 时，将 `.env.example` 复制为 `.env`，再填入密钥、服务地址和模型名。PowerShell 命令如下：

```powershell
Copy-Item .env.example .env
```

API 数据生成和评审可能产生费用。查看已保存结果无需密钥。

## 数据与使用范围

仓库实际包含角色对白文本和衍生数据。旧说明中“未分发原始版权材料”的表述无法覆盖这些文件。发布前需要逐项说明数据来源和再分发条件。

此次检查未发现仓库 `LICENSE`。代码、数据、模型和上游资源的使用条件需要分别确认。论文许可证不能替代仓库许可证。

引用格式见[英文 README](README.md#citation) 和 [CITATION.cff](CITATION.cff)。反馈问题时，请按[贡献说明](CONTRIBUTING.md)提供 Git 版本、Notebook 单元格、资源版本和错误信息。
