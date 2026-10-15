# 微分期产品风险分析（Micro-Installment Risk Analysis）

基于 100 份有效问卷的实证数据分析项目：用描述统计、卡方检验、Spearman 相关与回归模型识别微分期产品的关键风险因子，并输出可落地的产品风控设计。

## 核心发现（30 秒版）

- **分期意愿由"信任"与"冲动"驱动，而非经济能力**：多元回归 R²=0.280，官方信任 β=0.302（p=0.0002）影响最大，冲动消费 β=0.228（p=0.018）次之；生活费、可支配比例均不显著。
- **冲动消费是普遍现象**：74% 的受访者存在冲动消费倾向，且冲动倾向与冷静期接受度显著相关（χ²=13.93, p=0.008）。
- **信任缺失是最大障碍**：52% 的受访者对官方渠道"都怀疑"，信任与分期意愿显著相关（χ²=20.41, p=0.0004）。
- **"借新还旧"是关键高危信号**：5% 的受访者在资金不足时借新还旧，构成授信一票否决项的直接依据。
- **风险全景**：识别 15 项核心风险（12 项高风险），以"三层防线 + A/B/C 分层授信"应对，可还款余额 = 月生活费 × 可支配比例 × 0.39 − 现有月还款额。

## 仓库结构

```
micro-installment-risk-analysis/
├── README.md                  # 本文件
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   └── survey_raw.xlsx    # 原始问卷（100 份 × 13 题，已脱敏）
│   ├── processed/
│   │   └── survey_cleaned.xlsx# 清洗 + 量化编码后的分析数据
│   └── README.md              # 数据字典与隐私处理说明
├── notebooks/
│   ├── 01_data_cleaning.ipynb     # 数据清洗与量化编码（含清洗流程图）
│   ├── 02_eda_visualization.ipynb # 描述性统计与 13 张频数图
│   ├── 03_statistical_tests.ipynb # 卡方检验 + Spearman 相关
│   ├── 04_regression.ipynb        # 多元线性回归 + 有序 Logit + 结果导出
│   ├── 05_risk_matrix.ipynb       # R1–R15 风险矩阵图
│   └── 06_product_flow.ipynb      # 产品流程图
├── src/
│   ├── cleaning.py            # 清洗与量化编码模块
│   ├── stats_tests.py         # 卡方检验 / Spearman 模块
│   └── regression.py          # OLS / 有序 Logit 模块
├── results/
│   ├── charts/                # 16 张图（13 张频数图 + 流程图 + 风险矩阵 + 产品流程）
│   └── analysis_output.xlsx   # 分析结果汇总（描述统计/频数/相关/卡方/回归）
├── docs/
│   ├── methodology.md         # 研究方法论
│   ├── risk_register.md       # 风险清单与应对
│   └── product_design.md      # 产品设计要点
└── paper/
    └── README.md              # 研究报告说明
```

## 快速开始

```bash
pip install -r requirements.txt
# 运行 notebooks 另需：pip install jupyter

# 按顺序执行（每个 notebook 均可独立运行，从 data/ 读取上游产物）
jupyter nbconvert --to notebook --execute notebooks/01_data_cleaning.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_eda_visualization.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_statistical_tests.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_regression.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_risk_matrix.ipynb
jupyter nbconvert --to notebook --execute notebooks/06_product_flow.ipynb
```

- `01` 读取 `data/raw/survey_raw.xlsx`，产出 `data/processed/survey_cleaned.xlsx`；
- `02`–`04` 读取 processed 数据，图表写入 `results/charts/`，汇总结果写入 `results/analysis_output.xlsx`；
- `03`/`04` 复用 `src/` 中的检验与回归函数（`sys.path.append("../src")`）。

## 技术栈

pandas（清洗与统计）· scipy（卡方/Spearman）· statsmodels（OLS/有序 Logit）· matplotlib + seaborn（可视化）

## 数据与隐私

- 样本量 100 份（回收 127 份，剔除作答过短与逻辑矛盾样本后随机抽样）；
- 发布版数据已脱敏：移除了问卷平台元数据（序号、提交时间、作答时长、来源、IP），仅保留 13 道题的作答；
- 本仓库为数据分析研究项目，不包含任何可识别个人或机构的信息。

## 文档导航

| 想了解 | 去看 |
|--------|------|
| 问卷怎么设计的、数据怎么清洗的 | [docs/methodology.md](docs/methodology.md) |
| 有哪些风险、怎么应对 | [docs/risk_register.md](docs/risk_register.md) |
| 产品怎么设计的、依据是什么 | [docs/product_design.md](docs/product_design.md) |
| 数据字段含义 | [data/README.md](data/README.md) |
