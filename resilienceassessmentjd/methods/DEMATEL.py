# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :DEMATEL.py
# @Time      :2024/7/2 下午7:38
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np

from ..core.DecisionMethod import DecisionMethod


class DEMATEL(DecisionMethod):
    def __init__(self, parameters):
        data = np.array(parameters["data"])
        super().__init__(data)
        self.data = data

    def execute(self):
        """执行DEMATEL特定的计算."""
        # 确保数据是DEMATEL要求的方阵
        if self.data.shape[0] != self.data.shape[1]:
            return {"error": "DEMATEL data must be a square matrix."}

        # 计算归一化直接关系矩阵
        normalized_matrix = self.normalize_matrix(self.data)

        # 计算总关系矩阵
        total_relation_matrix = self.calculate_total_relation_matrix(normalized_matrix)
        if total_relation_matrix is None:
            return {
                "error": "Failed to compute total relation matrix. The matrix might not be invertible."
            }

        # 分析结果
        d, r = self.calculate_impact_degrees(total_relation_matrix)
        d_plus_r, d_minus_r = d + r, d - r

        return {
            "normalized_matrix": normalized_matrix.tolist(),
            "total_relation_matrix": total_relation_matrix.tolist(),
            "influence_degree": d.tolist(),
            "affected_degree": r.tolist(),
            "cause_degree": d_plus_r.tolist(),
            "effect_degree": d_minus_r.tolist(),
            "description": "DEMATEL method executed successfully.",
        }

    def normalize_matrix(self, matrix):
        """通过除以所有元素的和来使矩阵归一化."""
        matrix_sum = np.sum(matrix)
        if matrix_sum == 0:
            raise ValueError(
                "Sum of all elements in the matrix is zero, normalization impossible."
            )
        return matrix / matrix_sum

    def calculate_total_relation_matrix(self, normalized_matrix):
        """利用矩阵反演计算总关系矩阵."""
        I = np.eye(normalized_matrix.shape[0])  # Identity matrix
        try:
            return np.linalg.inv(I - normalized_matrix) - I
        except np.linalg.LinAlgError:
            return None

    def calculate_impact_degrees(self, total_relation_matrix):
        """计算影响程度(行和)和被影响程度(列和)."""
        d = np.sum(total_relation_matrix, axis=1)  # Impact degrees
        r = np.sum(total_relation_matrix, axis=0)  # Being impacted degrees
        return d, r
