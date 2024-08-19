# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Criterion.py
# @Time      :2024/7/18 上午9:25
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import pandas as pd

# from .ExceptionHandler import *
import traceback

class Criterion:
    """
    A class to represent a criterion for decision-making.

    Attributes
    ----------
    name : str
        The name of the criterion.
    weight : float
        The weight assigned to the criterion.
    values : list
        The values associated with the criterion.
    """

    def __init__(self, request):
        self.params = request.get('parameters')
        self.norm = request.get('normalization')
        self.assess_method = request.get("assess_method")
        self.data = self.params.get("data")
        self.criteria = self.params.get("criteria")
        self.criteria_dict = {item.pop('name'): item for item in self.criteria}
        self.criteria_names = tuple(self.criteria_dict.keys())
        self.params['criteria_dict'] = self.criteria_dict
        self.params['criteria_names'] = self.criteria_names
        self.df = None
        self.filled_df = None
        self.ids_area = None

    def get_criteria(self):
        try:
            self.check_data_format()
            self.params['init_data'] = self.df  # Add the original data to the parameters
            self.params['filled_data'] = self.filled_df  # Add the filled data to the parameters
            self.params['ids_area'] = self.ids_area
            """
            if self.assess_method == "MEE":
                level_boundaries = self.mee_level_boundaries(self.criteria_names)
                self.params['level_boundaries'] = level_boundaries
            """
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())



        return self.params

    # Get criterion MEE interval boundaries
    @staticmethod
    def mee_level_boundaries(criterion_list):
        boundaries = {
            "救灾类应急物资储备数量": {
                "待整改": (-38133.0, 170472.0),
                "合格": (170472.0, 337357.0),
                "良好": (337357.0, 504242.0),
                "优秀": (504242.0, 712847.0)
            },
            "救灾类临期应急物资处置数量": {
                "待整改": (7067.0, 4988.0),
                "合格": (4988.0, 3326.0),
                "良好": (3326.0, 1663.0),
                "优秀": (1663.0, -416.0)
            },
            "救灾类超期应急物资处置数量": {
                "待整改": (34851.0, 24601.0),
                "合格": (24601.0, 16400.0),
                "良好": (16400.0, 8200.0),
                "优秀": (8200.0, -2050.0)
            },
            "救灾类应急物资储备种类数": {
                "待整改": (5.0, 11.0),
                "合格": (11.0, 16.0),
                "良好": (16.0, 20.0),
                "优秀": (20.0, 26.0)
            },
            "救灾类临期应急物资种类数": {
                "待整改": (-0.0, 1.0),
                "合格": (1.0, 2.0),
                "良好": (2.0, 2.0),
                "优秀": (2.0, 3.0)
            },
            "救灾类过期应急物资种类数": {
                "待整改": (8.0, 5.0),
                "合格": (5.0, 4.0),
                "良好": (4.0, 2.0),
                "优秀": (2.0, 0.0)
            },
            "应急物资储备仓库的位置便利性": {
                "待整改": (0, 1),
                "合格": (1, 2),
                "良好": (2, 3),
                "优秀": (3, 5)
            },
            "建成区路网密度": {
                "待整改": (4.0, 5.0),
                "合格": (5.0, 6.0),
                "良好": (6.0, 8.0),
                "优秀": (8.0, 10.0)
            },
            "物流仓储用地面积": {
                "待整改": (1.0, 16.0),
                "合格": (16.0, 29.0),
                "良好": (29.0, 42.0),
                "优秀": (42.0, 57.0)
            },
            "救灾类应急物资供应商多元化程度": {
                "待整改": (30.0, 38.0),
                "合格": (38.0, 45.0),
                "良好": (45.0, 52.0),
                "优秀": (52.0, 61.0)
            },
            "救灾类应急物资产能响应时效": {
                "待整改": (9.0, 7.0),
                "合格": (7.0, 4.0),
                "良好": (4.0, 2.0),
                "优秀": (2.0, 0.0)
            },
            "应急物资储备形式多元化": {
                "待整改": (-0.5, 0.5),
                "合格": (-0.5, 0.5),
                "良好": (0.5, 1.5),
                "优秀": (0.5, 1.5)
            },
            "应急物资储备快速补仓产能": {
                "待整改": (768.0, 1666.0),
                "合格": (1666.0, 2385.0),
                "良好": (2385.0, 3103.0),
                "优秀": (3103.0, 4001.0)
            },
            "应急物资储备快速补仓周期": {
                "待整改": (24.0, 22.0),
                "合格": (22.0, 21.0),
                "良好": (21.0, 20.0),
                "优秀": (20.0, 18.0)
            },
            "防汛抗旱类应急物资储备数量": {
                "待整改": (0, 1828102.0),
                "合格": (1828102.0, 3656177.0),
                "良好": (3656177.0, 5484252.0),
                "优秀": (5484252.0, 7769347.0)
            },
            "防汛抗旱类临期应急物资处置数量": {
                "待整改": (124.0, 88.0),
                "合格": (88.0, 58.0),
                "良好": (58.0, 29.0),
                "优秀": (29.0, 0)
            },
            "防汛抗旱类超期应急物资处置数量": {
                "待整改": (138605.0, 97839.0),
                "合格": (97839.0, 65226.0),
                "良好": (65226.0, 32613.0),
                "优秀": (32613.0, 0)
            },
            "防汛抗旱类应急物资储备种类数": {
                "待整改": (0, 16.0),
                "合格": (16.0, 30.0),
                "良好": (30.0, 44.0),
                "优秀": (44.0, 62.0)
            },
            "防汛抗旱类临期应急物资种类数": {
                "待整改": (8, 6),
                "合格": (6, 4),
                "良好": (4, 2),
                "优秀": (2, 0)
            },
            "防汛抗旱类过期应急物资种类数": {
                "待整改": (34.0, 23.0),
                "合格": (23.0, 16.0),
                "良好": (16.0, 8.0),
                "优秀": (8.0, 0)
            },
            "应急物资储备仓库的位置便利性": {
                "待整改": (0, 1.0),
                "合格": (1.0, 2.0),
                "良好": (2.0, 3.0),
                "优秀": (3.0, 4.0)
            },
            "建成区路网密度": {
                "待整改": (2.0, 4.0),
                "合格": (4.0, 6.0),
                "良好": (6.0, 8.0),
                "优秀": (8.0, 10.0)
            },
            "物流仓储用地面积": {
                "待整改": (0, 16.0),
                "合格": (16.0, 28.0),
                "良好": (28.0, 41.0),
                "优秀": (41.0, 58.0)
            },
            "防汛抗旱类应急物资供应商多元化程度": {
                "待整改": (0.0, 3.0),
                "合格": (3.0, 6.0),
                "良好": (6.0, 8.0),
                "优秀": (8.0, 11.0)
            },
            "防汛抗旱类应急物资产能响应时效": {
                "待整改": (6.0, 5.0),
                "合格": (5.0, 4.0),
                "良好": (4.0, 3.0),
                "优秀": (3.0, 2.0)
            },
            "应急物资储备形式多元化": {
                "待整改": (-0.5, 0.5),
                "合格": (-0.5, 0.5),
                "良好": (0.5, 1.5),
                "优秀": (0.5, 1.5)
            },
            "应急物资储备快速补仓产能": {
                "待整改": (0, 22547.0),
                "合格": (22547.0, 45072.0),
                "良好": (45072.0, 67597.0),
                "优秀": (67597.0, 95753.0)
            },
            "应急物资储备快速补仓周期": {
                "待整改": (180.0, 90.0),
                "合格": (90.0, 45.0),
                "良好": (45.0, 15.0),
                "优秀": (15.0, 0.0)
            }
        }
        return {key: boundaries.get(key) for key in criterion_list}

    def check_data_format(self):
        # 将数据转换为DataFrame
        ids = [entry['id'] for entry in self.data]
        area = [entry['area'] for entry in self.data]
        value = [entry['value'] for entry in self.data]
        self.ids_area = dict(zip(ids, area))

        # 检查指标数量是否匹配
        if not all(len(item) == len(self.criteria_names) for item in value):
            return False
        # 创建DataFrame
        self.df = pd.DataFrame(value, index=ids, columns=self.criteria_names)
        self.filled_df = self.df.copy()
        # 检查是否存在空值
        if (self.filled_df == -99).values.any():
            # 用该列非-99值的均值填充-99
            for column in self.filled_df.columns:
                mean_value = self.filled_df[self.filled_df[column] != -99][column].mean()
                self.filled_df[column] = self.filled_df[column].replace(-99, mean_value)
