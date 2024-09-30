# !/usr/bin/env python
# @FileName  :Criterion.py
# @Time      :2024/7/18 上午9:25
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

# from .ExceptionHandler import *
import traceback

import numpy as np
import pandas as pd


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
        self.params = request.get("parameters")
        self.norm = request.get("normalization")
        self.assess_method = request.get("assess_method")
        self.data = self.params.get("data")
        self.criteria = self.params.get("criteria")
        self.criteria_dict = {item.pop("name"): item for item in self.criteria}
        self.criteria_names = tuple(self.criteria_dict.keys())
        self.invalid_ids = []
        self.df = None
        self.filled_df = None
        self.ids_area = None

    def get_criteria(self):
        try:
            self.check_data_format()
            self.params["criteria_dict"] = self.criteria_dict
            self.params["criteria_names"] = self.criteria_names
            self.params["init_data"] = (
                self.df
            )  # Add the original data to the parameters
            self.params["filled_data"] = (
                self.filled_df
            )  # Add the filled data to the parameters
            self.params["ids_area"] = self.ids_area
            self.params["invalid_ids"] = self.invalid_ids
            if self.assess_method == "MEE":
                level_boundaries = self.mee_level_boundaries()
                self.params["level_boundaries"] = level_boundaries
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())

        return self.params

    # Get criterion MEE interval boundaries
    @staticmethod
    def mee_level_boundaries():
        boundaries = {
            "应急物资储备仓库的位置便利性": {
                "待整改": (0, 1.0),
                "合格": (1.0, 2.0),
                "良好": (2.0, 3.0),
                "优秀": (3.0, 4.0),
            }
        }
        # 将 exist_boundaries 中的所有值转换为 np.float64
        for category, grades in boundaries.items():
            for grade, bounds in grades.items():
                boundaries[category][grade] = tuple(map(np.float64, bounds))

        return boundaries

    def check_data_format(self):
        # 将数据转换为DataFrame
        ids = [entry["id"] for entry in self.data]
        area = [entry["area"] for entry in self.data]
        value = [entry["value"] for entry in self.data]
        self.ids_area = dict(zip(ids, area, strict=False))
        # 检查指标数量是否匹配
        if not all(len(item) == len(self.criteria_names) for item in value):
            return False
        # 创建DataFrame
        self.df = pd.DataFrame(value, index=ids, columns=self.criteria_names)

        # 检查并移除所有数据均为-99的指标
        if not self.df.empty:
            # 检查是否整个 DataFrame 全部为 -99
            if (self.df == -99).all().all():
                raise ValueError("DataFrame contains only -99 values.")
            # 删除所有值均为-99的行和列
            self.df = self.df[(self.df != -99).any(axis=1)]  # 删除所有值均为-99的行
            self.df = self.df.loc[
                :, (self.df != -99).any(axis=0)
            ]  # 删除所有值均为-99的列

        else:
            raise ValueError("DataFrame is empty.")

        # 更新有效的指标列表，即在DataFrame中还存在的列
        self.criteria_names = tuple(self.df.columns)
        self.criteria_dict = {
            key: value
            for key, value in self.criteria_dict.items()
            if key in self.criteria_names
        }
        # 创建filled_df以进行后续处理
        self.filled_df = self.df.copy()

        # 判断filled_df是否存在一行都是-99
        if (self.filled_df == -99).all(axis=1).any():
            # 逐行检查是否存在一行都是-99
            for index, row in self.filled_df.iterrows():
                if (row == -99).all():
                    # 用1值填充该行
                    self.filled_df.loc[index] = 1
                    # 保存该行的index
                    self.invalid_ids.append(index)
        # 检查是否存在空值
        if (self.filled_df == -99).values.any():
            # 用该列非-99值的均值填充-99
            for column in self.filled_df.columns:
                mean_value = self.filled_df[self.filled_df[column] != -99][
                    column
                ].mean()
                self.filled_df[column] = self.filled_df[column].replace(-99, mean_value)
