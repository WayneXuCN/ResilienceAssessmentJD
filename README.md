# ResilienceAssessmentJD

## 简介

这是为应急物资物流仓储调配保障体系弹性评估项目开发的弹性评估模型`ResilienceAssessmentJD`的Python包，项目的目录结构展示在下方，包括所有必要组件，以及测试和文档该项目支持多种弹性评估方法，以帮助研究者和决策者评估和比较应急物资物流仓储调配保障体系的弹性。

```
ResilienceAssessmentJD/
├── ResilienceAssessmentJD/
│   ├── __init__.py
│   ├── __main__.py
│   ├── VERSION
│   ├── core/
│   │   ├── __init__.py
│   │   ├── UnifiedModel.py
│   │   ├── MethodFactory.py
│   │   ├── DecisionMethod.py
│   │   ├── ScalingMethod.py
│   │   └── ExceptionHandler.py
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── AHP.py
│   │   ├── CombinedMethod.py
│   │   ├── HEWM.py
│   │   ├── DEMATEL.py
│   │   ├── MACBETH.py
│   │   ├── EWM.py
│   │   ├── MEE.py
│   │   ├── PCA.py
│   │   └── VIKOR.py
│   └── cli.py
├── docs/
│   └── index.md
├── .github/
│   ├── release_message.sh
│   └── workflows/
├── .gitignore
├── HISTORY.md
├── LICENSE
├── Makefile
├── MANIFEST.in
├── mkdocs.yml
├── README.md
├── requirements.txt
├── requirements-test.txt
├── setup.py
└── tests/
    ├── conftest.py
    ├── __init__.py
    ├── test_core/
    │   └── test_unified_model.py
    └── test_methods/
        ├── test_ahp.py
        ├── test_dematel.py
        ├── test_ewm.py
        └── test_mee.py
```



```markdown
ResilienceAssessmentJD/
├── ResilienceAssessmentJD/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── UnifiedModel.py
│   │   ├── MethodFactory.py
│   │   ├── DecisionMethod.py
│   │   ├── ScalingMethod.py
│   │   └── ExceptionHandler.py
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── AHP.py
│   │   ├── CombinedMethod.py
│   │   ├── HEWM.py
│   │   ├── DEMATEL.py
│   │   ├── MACBETH.py
│   │   ├── EWM.py
│   │   ├── MEE.py
│   │   ├── PCA.py
│   │   └── VIKOR.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_ahp.py
│   │   ├── test_dematel.py
│   │   ├── test_ewm.py
│   │   └── test_mee.py
│   └── data/
│      ├── test_input.json
│      └── test_output.json
├── notebooks/
│   ├── example_analysis1.ipynb
│   └── example_analysis2.ipynb
├── dist/
│   ├── ResilienceAssessmentJD-0.1.0.tar.gz
│   └── ResilienceAssessmentJD-0.1.0-py3-none-any.whl
├── docs/
│   ├── installation_guide.md
│   ├── user_guide.md
│   └── api_documentation.md
├── README.md
├── LICENSE
├── pyproject.toml
├── MANIFEST.in
└── requirements.txt
```




- `ResilienceAssessmentJD/core`：核心代码模块。
  - `__init__.py`：初始化脚本，用于设置模块。
  - `UnifiedModel.py`：项目的入口文件，提供一个统一的接口用于执行弹性评估。 
  - `MethodFactory.py`：包含用于创建不同决策方法实例的工厂类。 
  - `DecisionMethods.py`：实现了多种决策方法的模块。 
  - `ScalingMethod.py`：实现多种数据处理方法的模块
  - `Criterion.py`: 为不同的模型提供了统一的数据接口，确保了数据处理的一致性和可靠性。
  - `ExceptionHandler.py`：提供一个异常处理器，用于处理异常情况。
- `ResilienceAssessmentJD/methods`：具体方法实现
- `ResilienceAssessmentJD/tests/`：包含所有单元测试。
  - `__init__.py`：初始化测试模块。 
- `notebooks/`：包含示例 Jupyter 笔记本。
  - `example_analysis1.ipynb`：示例分析1。
  - `example_analysis2.ipynb`：示例分析2。
- `ResilienceAssessmentJD/data/`：存储测试输入和输出的示例数据。 
  - `test_input.json`：示例输入 JSON 数据。 
  - `test_output.json`：从测试输入预期的输出 JSON 数据。
- `docs/`：详细的项目文档，包括安装指南、用户指南、API文档等。
- `README.md`：项目概述和快速开始指南。
- `requirements.txt`：列出所有依赖项，用于配置项目环境。

## 快速开始

以下是一个简单的例子，展示如何使用本库进行基础的弹性评估：

```python
import json
from ResilienceAssessmentJD.core import UnifiedModel

test_input_path = "ResilienceAssessmentJD/data/data_防汛仓_京津冀_排序.json"
with open(test_input_path, 'r', encoding='utf-8') as file:
    request_json = json.load(file)

model = UnifiedModel(request_json)
result = model.execute()
# 保存结果为Json
with open("ResilienceAssessmentJD/data/防汛仓_京津冀_排序_result.json", 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)
```

## 测试

本项目使用 pytest 进行单元测试。