# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :HEWM.py
# @Time      :2024/7/10 下午7:03
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np

from ..core.DecisionMethod import DecisionMethod
import traceback
# from ..core.ExceptionHandler import *


class HEWM(DecisionMethod):
    """Hierarchical Equal Weighting Method

    """

    def __init__(self, params):
        super().__init__(params)
        self.weights = np.full(self.df.shape, 1 / self.df.shape[1])

    def execute(self):
        """
        Execute the Hierarchical Equal Weighting Method (HEWM).
        Criteria with missing values are automatically ignored and equal weights are automatically assigned to valid criteria.
        """
        try:
            # 缺失值的位置
            mask = (self.df == -99)
            # 将缺失值位置的权重设为 0
            self.weights[mask] = 0
            # 计算每个评估对象的有效指标数量
            valid_criteria_counts = np.count_nonzero(self.weights, axis=1)
            # 避免除以零的错误
            valid_criteria_counts = np.where(valid_criteria_counts == 0, 1, valid_criteria_counts)
            # 创建新的等权矩阵, 将缺失值修改为0
            new_weight = (1 / valid_criteria_counts[:, np.newaxis]) * np.ones((1, self.df.shape[1]))
            new_weight[mask] = 0
            return {"status": "success", "weights": new_weight.tolist()}
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())
