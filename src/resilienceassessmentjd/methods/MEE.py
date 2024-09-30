# !/usr/bin/env python
# @FileName  :MEE.py
# @Time      :2024/7/2 下午7:54
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import copy
import traceback

import numpy as np
import pandas as pd

from ..core.DecisionMethod import DecisionMethod


class MEE(DecisionMethod):
    """
    Matter-Element Extension Model.

    This class implements the Matter-Element Extension Model for decision-making.
    """

    def __init__(self, params):
        super().__init__(params)

    def preprocess_data(self, df_chosed):
        """
        If level_boundaries exists in params, it is used directly.

        Otherwise, a default level_boundaries is calculated.
        Calculate the mean and standard deviation of each criterion.
        Divide into four levels according to the mean and standard deviation:
        to be rectified, qualified, good, and excellent.

        In order to divide into four levels, you can choose n = 0.5, 1, 1.5, 2.
        """
        # Check for unique values in each column
        unique_values = {
            column: df_chosed[column].unique() for column in df_chosed.columns
        }
        # n_values = [0.5, 1, 1.5, 2]
        attribute_0 = self.get_keys_by_value(
            self.params["criteria_dict"], "attribute", "0"
        )
        attribute_1 = self.get_keys_by_value(
            self.params["criteria_dict"], "attribute", "1"
        )
        attribute_2 = self.get_keys_by_value(
            self.params["criteria_dict"], "attribute", "2"
        )
        level_boundaries = {}
        for column, _ in unique_values.items():
            # For other indicators, use the 25th, 50th, and 75th percentiles to divide the grades
            max_val, min_val = df_chosed[column].max(), df_chosed[column].min()
            interval = (max_val - min_val) / 4
            round_digits = 2
            if column in attribute_0:
                level_boundaries[column] = {
                    "待整改": (
                        round(min_val - 0.5 * interval, round_digits),
                        round(min_val + 1 * interval, round_digits),
                    ),
                    "合格": (
                        round(min_val + 1 * interval, round_digits),
                        round(min_val + 2 * interval, round_digits),
                    ),
                    "良好": (
                        round(min_val + 2 * interval, round_digits),
                        round(min_val + 3 * interval, round_digits),
                    ),
                    "优秀": (
                        round(max_val - 1 * interval, round_digits),
                        round(max_val + 0.5 * interval, round_digits),
                    ),
                }
            elif column in attribute_1:
                level_boundaries[column] = {
                    "待整改": (
                        round(max_val - 1 * interval, round_digits),
                        round(max_val + 0.5 * interval, round_digits),
                    ),
                    "合格": (
                        round(max_val - 2 * interval, round_digits),
                        round(max_val - 1 * interval, round_digits),
                    ),
                    "良好": (
                        round(max_val - 3 * interval, round_digits),
                        round(max_val - 2 * interval, round_digits),
                    ),
                    "优秀": (
                        round(min_val - 0.5 * interval, round_digits),
                        round(min_val + 1 * interval, round_digits),
                    ),
                }
            elif column in attribute_2:
                level_boundaries[column] = {
                    "待整改": (-0.5, 0.5),
                    "合格": (-0.5, 0.5),
                    "良好": (0.5, 1.5),
                    "优秀": (0.5, 1.5),
                }
        return level_boundaries

    def perform_computation(self, level_boundaries, df_chosed):
        """
        Perform the specific computation for the MEE method.

        Returns
        -------
        result : dict
            The result of the computation.
        """
        try:
            correlation_degrees = {}
            for column_name, column_data in df_chosed.items():
                # 读取经典域
                boundary = level_boundaries.get(column_name)
                # 读取节域
                all_values = [
                    item for sublist in boundary.values() for item in sublist
                ]  # 元素提取出来并扁平化到一个列表中
                _min, _max = min(all_values), max(all_values)
                _corr = []
                for i in boundary:
                    lower, upper = boundary.get(i)
                    # 计算关联度
                    # 经典域物元距离
                    distance_cla = np.abs(column_data - 0.5 * (lower + upper)) - 0.5 * (
                        upper - lower
                    )
                    # 节域物元距离1
                    distance_ext = np.abs(column_data - 0.5 * (_min + _max)) - 0.5 * (
                        _max - _min
                    )
                    # 使用布尔索引检查指标的值是否在经典域物元区间内
                    is_in_range = (distance_cla >= lower) & (distance_cla <= upper)
                    # 检查是否存在相等的距离
                    equal_distances = np.isclose(distance_cla, distance_ext)
                    # 利用向量化运算计算关联度
                    _epsilon = 1e-10  # 防止除以0
                    _corr.append(
                        pd.Series(
                            np.where(
                                is_in_range,
                                -distance_cla
                                / np.clip(np.abs(upper - lower), _epsilon, None),
                                # 使用 np.clip() 函数来限制最小分母值
                                np.where(
                                    equal_distances,
                                    0,  # 当距离相等时，关联度设为0
                                    distance_cla / (distance_ext - distance_cla),
                                ),
                            ),
                            name=i,
                            index=is_in_range.index,
                        )
                    )
                _corr = pd.concat(_corr, axis=1)
                _corr["分类等级"] = _corr.idxmax(axis=1)
                # 重命名索引列
                _corr.reset_index(inplace=True)
                # 重命名索引列
                _corr.rename(columns={"index": "评估对象"}, inplace=True)
                correlation_degrees[column_name] = _corr
            return correlation_degrees
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())

    def execute(self):
        """
        Execute the Matter-Element Extension Model (MEE).

        Returns
        -------
        result : list
            The result of the MEE execution.
        """
        try:
            df_chosed = self.norm_df
            # df_chosed = self.filled_df
            # 读取自动设置的经典域
            level_boundaries = self.preprocess_data(df_chosed)
            # 更新手动设置的经典域
            exist_boundaries = self.params.get("level_boundaries")
            # 检查并更新存在的键
            for key, boundaries in exist_boundaries.items():
                if key in level_boundaries:
                    level_boundaries[key] = boundaries

            correlation_degrees = self.perform_computation(level_boundaries, df_chosed)

            weights = pd.DataFrame(
                self.params["weights"].copy(),
                columns=self.params["criteria_names"],
                index=self.params["ids_area"].keys(),
            )
            ids_area = self.params["ids_area"]
            criteria_dict = self.params["criteria_dict"]

            elements = {
                f"E{i}": self.get_keys_by_value(criteria_dict, "element", f"E{i}")
                for i in range(1, 4)
            }
            dimensions = {
                f"D{i}": self.get_keys_by_value(criteria_dict, "dimension", f"D{i}")
                for i in range(1, 4)
            }
            corr_comp = {
                f"{d}_{e}": pd.DataFrame()
                for d in ["D1", "D2", "D3"]
                for e in ["E1", "E2", "E3"]
            }
            corr_comp.update({f"E{i}": pd.DataFrame() for i in range(1, 4)})

            result = []
            for criterion, data in correlation_degrees.items():
                corr_criterion = data[["待整改", "合格", "良好", "优秀"]] * weights[
                    criterion
                ].values.reshape(-1, 1)
                for d, d_criteria in dimensions.items():
                    if criterion in d_criteria:
                        for e, e_criteria in elements.items():
                            if criterion in e_criteria:
                                key = f"{d}_{e}"
                                corr_comp[key] = self.add_to_df(
                                    corr_comp[key], corr_criterion
                                )
                for e, e_criteria in elements.items():
                    if criterion in e_criteria:
                        corr_comp[e] = self.add_to_df(corr_comp[e], corr_criterion)
            for key, value in corr_comp.items():
                value = copy.deepcopy(value)
                if value.empty:
                    continue
                value["分类等级"] = value.idxmax(axis=1)
                value["评估对象"] = list(ids_area.keys())

                if key in ["E1", "E2", "E3"]:
                    for _id, area in ids_area.items():
                        if _id in self.params["invalid_ids"]:
                            score = {
                                "id": _id,
                                "area": area,
                                "type": "要素评估",
                                "element": key,
                                "rectified_value": "/",
                                "qualified_value": "/",
                                "good_value": "/",
                                "excellent_value": "/",
                                "level": "/",
                            }
                        else:
                            score = {
                                "id": _id,
                                "area": area,
                                "type": "要素评估",
                                "element": key,
                                "rectified_value": value.loc[
                                    value["评估对象"] == _id, "待整改"
                                ].values[0],
                                "qualified_value": value.loc[
                                    value["评估对象"] == _id, "合格"
                                ].values[0],
                                "good_value": value.loc[
                                    value["评估对象"] == _id, "良好"
                                ].values[0],
                                "excellent_value": value.loc[
                                    value["评估对象"] == _id, "优秀"
                                ].values[0],
                                "level": value.loc[
                                    value["评估对象"] == _id, "分类等级"
                                ].values[0],
                            }
                        result.append(score)
                elif key.split("_")[0] in ["D1", "D2", "D3"] and key.split("_")[1] in [
                    "E1",
                    "E2",
                    "E3",
                ]:
                    for _id, area in ids_area.items():
                        if _id in self.params["invalid_ids"]:
                            score = {
                                "id": _id,
                                "area": area,
                                "type": "维度评估",
                                "dimension": key.split("_")[0],
                                "element": key.split("_")[1],
                                "rectified_value": "/",
                                "qualified_value": "/",
                                "good_value": "/",
                                "excellent_value": "/",
                                "level": "/",
                            }
                        else:
                            score = {
                                "id": _id,
                                "area": area,
                                "type": "维度评估",
                                "dimension": key.split("_")[0],
                                "element": key.split("_")[1],
                                "rectified_value": value.loc[
                                    value["评估对象"] == _id, "待整改"
                                ].values[0],
                                "qualified_value": value.loc[
                                    value["评估对象"] == _id, "合格"
                                ].values[0],
                                "good_value": value.loc[
                                    value["评估对象"] == _id, "良好"
                                ].values[0],
                                "excellent_value": value.loc[
                                    value["评估对象"] == _id, "优秀"
                                ].values[0],
                                "level": value.loc[
                                    value["评估对象"] == _id, "分类等级"
                                ].values[0],
                            }
                        result.append(score)

            # 计算综合评估结果
            corr_comp = pd.DataFrame()
            for criterion, data in correlation_degrees.items():
                corr_criterion = data[["待整改", "合格", "良好", "优秀"]] * weights[
                    criterion
                ].values.reshape(-1, 1)
                corr_comp = self.add_to_df(corr_comp, corr_criterion)

            corr_comp["分类等级"] = corr_comp.idxmax(axis=1)
            corr_comp["评估对象"] = list(ids_area.keys())

            for _id, area in ids_area.items():
                if _id in self.params["invalid_ids"]:
                    compre_score = {
                        "id": _id,
                        "area": area,
                        "type": "综合评估",
                        "rectified_value": "/",
                        "qualified_value": "/",
                        "good_value": "/",
                        "excellent_value": "/",
                        "level": "/",
                    }
                else:
                    compre_score = {
                        "id": _id,
                        "area": area,
                        "type": "综合评估",
                        "rectified_value": corr_comp.loc[
                            corr_comp["评估对象"] == _id, "待整改"
                        ].values[0],
                        "qualified_value": corr_comp.loc[
                            corr_comp["评估对象"] == _id, "合格"
                        ].values[0],
                        "good_value": corr_comp.loc[
                            corr_comp["评估对象"] == _id, "良好"
                        ].values[0],
                        "excellent_value": corr_comp.loc[
                            corr_comp["评估对象"] == _id, "优秀"
                        ].values[0],
                        "level": corr_comp.loc[
                            corr_comp["评估对象"] == _id, "分类等级"
                        ].values[0],
                    }
                result.append(compre_score)

            return result

        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())

    @staticmethod
    def get_keys_by_value(d, value_key, target_value):
        return [k for k, v in d.items() if v[value_key] == target_value]

    @staticmethod
    def add_to_df(df, new_data):
        return new_data if df.empty else df + new_data
