# !/usr/bin/env python
# @FileName  :EWM.py
# @Time      :2024/7/2 下午7:39
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np

from ..core.DecisionMethod import DecisionMethod


class EWM(DecisionMethod):
    def __init__(self, params):
        super().__init__(params)
        # Data type: 1 indicates a positive criterion, 0 indicates a negative criterion
        self.data_types = params.get("data_types", [1] * self.norm_df.shape[1])

    def execute(self):
        """执行熵权法计算."""
        if len(self.data_types) != self.norm_df.shape[1]:
            return {
                "error": "The number of indicator types does not match the number of data columns."
            }

        # 标准化数据
        normalized_data = self.normalize_data(self.norm_df)
        # 计算熵值
        entropy = self.calculate_entropy(normalized_data)
        # 计算权重
        weights = self.calculate_weights(entropy)
        # 计算加权结果
        # weighted_result = (self.norm_df * weights).sum(axis=1)

        return weights.tolist()

    def normalize_data(self, data):
        """标准化数据,正指标不变,负指标取倒数"""
        for i in range(data.shape[1]):
            if self.data_types[i] == 0:  # 负向指标
                data[:, i] = 1 / data[:, i]
            # 防止除以0的错误
            data[:, i] = np.nan_to_num(data[:, i], nan=0.0, posinf=0.0, neginf=0.0)
        return data

    @staticmethod
    def calculate_entropy(self, normalized_data):
        """计算每个准则的熵.."""
        epsilon = np.finfo(float).eps  # Small constant to avoid log(0)
        entropy = -np.sum(
            normalized_data * np.log(normalized_data + epsilon), axis=0
        ) / np.log(len(normalized_data))
        return entropy

    @staticmethod
    def calculate_weights(self, entropy):
        """根据熵值计算权重."""
        redundancy = 1 - entropy
        weights = redundancy / redundancy.sum()
        return weights
