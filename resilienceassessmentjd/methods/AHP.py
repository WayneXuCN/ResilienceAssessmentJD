# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :AHP.py
# @Time      :2024/5/16 下午2:07
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np
from ..core.ExceptionHandler import *
from ..core.DecisionMethod import DecisionMethod


class AHP(DecisionMethod):
    def __init__(self, params):
        super().__init__(params)
        # Get the AHP data matrix
        self.ahp_params = params.get("ahp_params", {})

    def execute(self):
        """AHP 特定的执行逻辑"""
        if not self._is_positive_reciprocal_matrix(self.ahp_params):
            return {
                "error": "Data does not meet the positive reciprocal matrix requirement."
            }
        eigenvalues, eigenvectors = np.linalg.eig(self.ahp_params)
        max_index = np.argmax(eigenvalues)
        max_eigenvalue = eigenvalues[max_index].real
        eigenvector = eigenvectors[:, max_index].real
        weights = eigenvector / eigenvector.sum()
        consistency_ratio = self._calculate_consistency_ratio(max_eigenvalue)

        return {"status": "success", "weights": weights.round(4).tolist()}

    @staticmethod
    def _is_positive_reciprocal_matrix(self, matrix):
        """检查矩阵是否正反矩阵."""
        return np.allclose(matrix, 1 / matrix.T, atol=1e-10)

    def _calculate_consistency_ratio(self, max_eigenvalue):
        """计算AHP矩阵的一致性比."""
        size = self.data.shape[0]
        random_indices = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        CI = (max_eigenvalue - size) / (size - 1)
        RI = (
            random_indices[size] if size < len(random_indices) else 1.51
        )  # Default RI value for larger matrices
        return CI / RI if RI != 0 else 0