"""
ResilienceAssessmentJD - A Python library for assessing and comparing the
resilience of emergency material logistics storage and allocation systems.

This library supports multiple resilience assessment methods and provides
a unified interface for various decision-making approaches.
"""

from .core import (
    DecisionMethod,
    DecisionMethodFactory,
    ExceptionHandler,
    ScalingMethod,
    ScalingMethodFactory,
    UnifiedModel,
)

__version__ = "1.0.0"
__author__ = "Wenjie Xu <wenjie.xu.cn@outlook.com>"

__all__ = [
    "UnifiedModel",
    "DecisionMethodFactory",
    "ScalingMethodFactory",
    "DecisionMethod",
    "ScalingMethod",
    "ExceptionHandler",
]
