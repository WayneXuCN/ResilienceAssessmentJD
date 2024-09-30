# !/usr/bin/env python
# @FileName  :CombinedMethod.py
# @Time      :2024/7/10 下午7:04
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import numpy as np

from ..core.DecisionMethod import DecisionMethod


class CombinedMethod(DecisionMethod):
    # TODO: Implement Weight Combined Method

    def __init__(self, parameters):
        self.subj_weights = np.array(parameters["subjective_weights"])
        self.obj_weights = np.array(parameters["objective_weights"])

    def execute(self):
        combined_weights = (self.subj_weights + self.obj_weights) / 2  # 简单平均
        return combined_weights.tolist()
