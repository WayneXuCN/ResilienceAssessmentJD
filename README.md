# ResilienceAssessmentJD

[![Python 版本](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![代码风格](https://img.shields.io/badge/code%20style-ruff-orange)](https://docs.astral.sh/ruff/)

## 概述

ResilienceAssessmentJD 是一个用于评估和比较应急物资物流仓储调配保障体系弹性的 Python 库，提供了一个灵活且可扩展的平台，用于进行多标准决策分析。

该框架支持多种评估方法，并提供统一接口以确保评估过程的一致性。它使用户能够根据自定义标准执行分类评估、自审评估和排序评估。

## 主要特性

- **多方法支持**：实现了多种决策方法，包括 AHP、DEMATEL、EWM、MACBETH、MEE、PCA 和 VIKOR
- **模块化架构**：通过工厂模式和统一模型接口实现关注点的清晰分离
- **可扩展设计**：易于添加新的评估方法和缩放技术
- **错误处理**：具有详细错误报告的健壮异常处理机制
- **命令行界面**：用于批处理的简单命令行接口

## 项目结构

```
弹性评估框架/
├── src/
│   └── resilienceassessmentjd/
│       ├── __init__.py
│       ├── __main__.py           # 主入口点
│       ├── cli.py                # 命令行接口
│       ├── core/                 # 核心框架组件
│       │   ├── __init__.py
│       │   ├── UnifiedModel.py   # 中心协调器
│       │   ├── MethodFactory.py  # 方法的工厂模式
│       │   ├── DecisionMethod.py # 决策方法基类
│       │   ├── ScalingMethod.py  # 数据预处理方法
│       │   ├── Criterion.py      # 数据结构化
│       │   └── ExceptionHandler.py # 错误管理
│       └── methods/              # 评估方法的实现
│           ├── __init__.py
│           ├── AHP.py            # 层次分析法
│           ├── CombinedMethod.py # 混合加权方法
│           ├── DEMATEL.py        # DEMATEL
│           ├── EWM.py            # 熵权法
│           ├── HEWM.py           # 混合熵权法
│           ├── MACBETH.py        # MACBETH
│           ├── MEE.py            # 物元可拓法
│           ├── PCA.py            # 主成分分析
│           └── VIKOR.py          # 多准则优化与妥协解
├── data/                         # 示例数据文件
├── .gitignore
├── LICENSE
├── pyproject.toml                # 项目配置
├── README.md                     # 本文件
└── uv.lock                       # 依赖锁定文件
```

## 安装

### 通过 pip 安装（推荐）

您可以直接安装已发布的版本：

```bash
pip install resilienceassessmentjd
```

或者，如果您在 GitHub 上的 releases 中提供了预构建的包，也可以通过以下方式安装：

```bash
pip install https://github.com/WayneXuCN/ResilienceAssessmentJD/releases/download/v1.0.0/resilienceassessmentjd-1.0.0-py3-none-any.whl
```

### 从源码安装

本项目使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理和打包。首先，请确保您已安装 `uv`，安装项目依赖：

```bash
git clone https://github.com/WayneXuCN/ResilienceAssessmentJD.git
cd ResilienceAssessmentJD
uv sync
```

## 使用方法

### 通过命令行工具使用（推荐）

安装完成后，您可以直接使用命令行工具：

```bash
resilience-assessment <输入文件> <输出目录>
```

示例：

```bash
resilience-assessment data/sample_data.json results/
```

### 使用 uv 运行

如果您使用 uv 安装了依赖，可以使用以下命令运行：

```bash
uv run -m resilienceassessmentjd <输入文件> <输出目录>
```

示例：

```bash
uv run -m resilienceassessmentjd data/sample_data.json results/
```

### 作为 Python 模块使用

您也可以在 Python 代码中直接使用：

```python
from resilienceassessmentjd.core.UnifiedModel import UnifiedModel
import json

# 读取输入数据
with open('data/sample_data.json', 'r', encoding='utf-8') as f:
    request_json = json.load(f)

# 初始化模型并执行
model = UnifiedModel(request_json)
result = model.execute()

# 处理结果
print(result)
```

### 输入数据格式

框架期望以下结构的 JSON 输入：

```json
{
  "assess_type": "classification|ranking|self_assessment",
  "weight_method": {
    "subjective_method": "HEWM|AHP",
    "objective_method": "EWM|PCA",
    "combined_method": "CombinedMethod"
  },
  "normalization": "MinMax|BRM",
  "assess_method": "MEE|VIKOR|MACBETH",
  "parameters": {
    "criteria": [
      {
        "name": "准则名称",
        "dimension": "D1|D2|D3",
        "element": "E1|E2|E3",
        "attribute": "0|1|2"  // 0: 效益型, 1: 成本型, 2: 固定型
      }
    ],
    "data": [
      {
        "id": "对象ID",
        "value": [/* 准则值数组 */],
        "period": "时间周期",
        "area": "区域代码"
      }
    ]
  }
}
```

### 支持的评估类型

1. **分类评估**：根据性能水平对对象进行分类
2. **排序评估**：对对象进行相对排名
3. **自审评估**：评估对象在多个时间周期的表现

## 许可证

本项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。

## 致谢

该框架是作为推进**应急物资物流仓储调配保障体系**弹性评估的研究计划的一部分而开发的。
