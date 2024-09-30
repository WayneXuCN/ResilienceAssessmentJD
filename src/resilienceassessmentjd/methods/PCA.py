# !/usr/bin/env python
# @FileName  :PCA.py.py
# @Time      :2024/7/2 下午7:39
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np

from ..core.DecisionMethod import DecisionMethod


class PCA(DecisionMethod):
    def __init__(self, parameters):
        data = np.array(parameters["data"])
        super().__init__(data)
        self.data = data

    def execute(self):
        """执行主成分分析."""
        data = np.array(self.data)
        if data.size == 0 or np.any(np.isnan(data)):
            return {
                "error": "Data cannot be empty and must not contain NaN values for PCA."
            }

        # 标准化数据(均值=0,方差=1)
        standardized_data = self.standardize_data(data)

        # 计算协方差矩阵
        covariance_matrix = np.cov(standardized_data, rowvar=False)

        # 计算特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

        # 按降序对特征值和特征向量进行排序
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        # 选择前N个特征向量(主成分),N可以根据特征值准则定义
        num_components = self.select_number_of_components(eigenvalues)
        principal_components = eigenvectors[:, :num_components]

        # 将数据投影到主成分上
        projected_data = np.dot(standardized_data, principal_components)

        return {
            "explained_variance": eigenvalues[:num_components].tolist(),
            "components": principal_components.tolist(),
            "projected_data": projected_data.tolist(),
            "description": "PCA method executed successfully.",
        }

    def standardize_data(self, data):
        """将数据标准化,使其均值为零,方差为1"""
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        standardized_data = (data - mean) / std
        return standardized_data

    def select_number_of_components(self, eigenvalues):
        """选择主成分的个数.该标准可以基于已解释方差."""
        total_variance = np.sum(eigenvalues)
        variance_covered = 0.0
        num_components = 0
        for eigenvalue in eigenvalues:
            variance_covered += eigenvalue
            num_components += 1
            if (
                variance_covered / total_variance >= 0.95
            ):  # 95% variance covered criterion
                break
        return num_components
