# Qwen3.5-35B-A3B CountBenchQA 复现实验

[English](README.md) · [实验协议](docs/EXPERIMENT_PROTOCOL.md) · [评分规则](docs/EVALUATION.md) · [详细结果](docs/RESULTS.md) · [复现步骤](docs/REPRODUCE.md)

本仓库记录 **Qwen3.5-35B-A3B** 在修订版 **CountBenchQA** 上的最终实验：**AWQ 4-bit／非量化 16-bit（BF16）** × **think／nothink**。think 下每种模型进行一次完整推理；nothink 下每种模型进行三次独立推理并报告三轮平均值。八轮实验均包含 487 个样本的完整原始输出、独立最终答案、token 统计和统一评分。

## 最终实验结果

采用 VLMEvalKit CountBenchQA 官方最终答案子串规则：`ans in pred`。`pred` 仅为最终答案文本，不包含思考过程。

| 模型 | 模式 | 独立轮数 | 正确数／487 | 准确率 | 平均输出 token／题 | 中位数 | 最大值 |
|---|---|---:|---:|---:|---:|---:|---:|
| AWQ 4-bit | think | 1 | 472/487 | **96.92%** | 952.06 | 341 | 30,627 |
| AWQ 4-bit | nothink | 3 | 439.67/487（三轮均值） | **90.28%** | 2.10 | 2 | 3 |
| 非量化 16-bit（BF16） | think | 1 | 468/487 | **96.10%** | 923.02 | 313 | 39,865 |
| 非量化 16-bit（BF16） | nothink | 3 | 444.67/487（三轮均值） | **91.31%** | 2.12 | 2 | 3 |

nothink 的三轮准确率分别独立计算后再等权平均；每轮均为 487 条，因此也等于合并 1,461 条预测后的准确率：AWQ 为 1,319/1,461，BF16 为 1,334/1,461。**没有多数投票、每题取优或 best-of-N。**逐轮结果见 [`results/summary/run_level_summary.csv`](results/summary/run_level_summary.csv)。

输出 token 包含思考和最终答案，是生成工作量与推理链长度指标，不是跨硬件速度指标。nothink 最终表的中位数、分位数和最大值基于三轮合并输出计算。

## 数据集下载与来源

- **本实验实际使用的修订版 TSV：**[直接下载 CountBenchQA.tsv](https://opencompass.openxlab.space/utils/VLMEval/CountBenchQA.tsv)，共 487 条，MD5 为 `fc73c8d4ffa665431448753f094d56ff`。
- **评测来源框架：**[OpenCompass VLMEvalKit](https://github.com/open-compass/VLMEvalKit)。
- **上游数据集页面：**[Hugging Face CountBenchQA](https://huggingface.co/datasets/vikhyatk/CountBenchQA)。
- 本地下载与校验说明：[`data/README.md`](data/README.md)。

## 共同协议

- 数据：487 条修订版 CountBenchQA，MD5 `fc73c8d4ffa665431448753f094d56ff`；图像使用 TSV 原始 base64 字节，不手工缩放、压缩或裁剪。
- Prompt：原始 `question` 加以下固定后缀，无 system message、few-shot 或答案信息。

```text
 Note that: answer with a number directly e.g. 3. Do not include any additional text.
```

- 共同采样：`temperature=1.0`、`top_p=0.95`、`top_k=20`、`repetition_penalty=1.0`。
- 随机数：BF16 think 使用 seed 0，BF16 nothink 依次使用 seed 0、1、2，均在每个样本生成前设置；AWQ think 和 nothink 首轮未固定 seed，nothink 另外两轮固定 seed 1、2。
- 配置差异：AWQ 使用 vLLM 0.32.0、`presence_penalty=1.5`；BF16 使用 Transformers 5.22.1、SDPA、`presence_penalty=0.0`。
- 完整性：八轮均为 487 个唯一样本，样本 ID 跨轮对齐，完整原始输出齐全，最终记录均自然结束。

详细设置见 [`configs/`](configs/) 和 [`docs/EXPERIMENT_PROTOCOL.md`](docs/EXPERIMENT_PROTOCOL.md)。

## 校验与复现

```bash
python3 scripts/verify_results.py
bash data/download.sh
```

第一条命令无需 GPU，会逐轮复算指标、检查完整原始输出，并重新计算 nothink 三轮平均。重新生成见 [`docs/REPRODUCE.md`](docs/REPRODUCE.md)。仓库不直接包含模型权重、数据 TSV 或图像缓存。

## 目录

```text
configs/                 四种最终配置的机器可读协议与逐轮随机数策略
data/                    数据下载与 MD5 校验
docs/                    实验、评分、结果、字段与复现文档
environment/             软件与依赖快照
results/final/           八轮完整原始输出和最终答案
results/summary/         最终结果、逐轮指标与逐样本对照
scripts/                 推理、评分和完整性校验代码
```

BF16 模型为 [Qwen/Qwen3.5-35B-A3B](https://huggingface.co/Qwen/Qwen3.5-35B-A3B)，AWQ 模型为 `QuantTrio/Qwen3.5-35B-A3B-AWQ`；评分上游为 [VLMEvalKit](https://github.com/open-compass/VLMEvalKit)。原创代码和文档采用 [MIT License](LICENSE)，第三方资产遵循各自许可。
