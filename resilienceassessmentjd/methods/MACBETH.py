# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :MACBETH.py
# @Time      :2024/7/3 上午10:00
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import traceback

import numpy as np
import pandas as pd
from collections import defaultdict
import re

from ..core.DecisionMethod import DecisionMethod


class MACBETH(DecisionMethod):
    """
    MACBETH Model.

    This class implements the MACBETH (Measuring Attractiveness by a Categorical Based Evaluation Technique) Model for decision-making.
    """

    def __init__(self, params):
        super().__init__(params)
        self.id_list = [f'{i["id"]}_{i["period"]}' for i in self.params.get("data", [])]
        self.norm_df.index = self.id_list
        self.filled_df.index = self.id_list
        self.weights = pd.DataFrame(self.params["weights"].copy(), columns=self.params['criteria_names'],
                                    index=self.id_list)
        self.ids_area = self.params["ids_area"]
        self.criteria_dict = self.params['criteria_dict']
        self.criteria_types = {key: value.get('attribute') for key, value in self.criteria_dict.items()}
        """
        # For negative indicators (type 1), a 1-x conversion is required
        for key, value in self.criteria_types.items():
            if value == '1':
                self.norm_df[key] = 1 - self.norm_df[key]
        """

    def preprocess_data(self, data):
        n, m = data.shape
        pairwise_comparisons = {}
        for criterion in data.columns:
            column_data = data[criterion]
            attr_type = self.criteria_types[criterion]

            for i in range(n):
                for j in range(i + 1, n):
                    option1 = data.index[i]
                    option2 = data.index[j]

                    if attr_type == '0':  # 正向指标
                        diff = column_data[option1] - column_data[option2]
                    elif attr_type == '1':  # 负向指标
                        diff = column_data[option2] - column_data[option1]
                    else:  # 0/1变量
                        diff = abs(column_data[option1] - column_data[option2])

                    # 将差异标准化到0-6的范围，对应MACBETH的7个类别
                    if attr_type == '2':
                        normalized_diff = 6 * diff  # 对于0/1变量，差异只有0或1
                    else:
                        std = column_data.std()
                        if std == 0 or np.isnan(std) or np.isnan(diff):
                            normalized_diff = 0  # 如果标准差为0或有NaN值，视为无差异
                        else:
                            normalized_diff = 3 + 3 * np.tanh(diff / std)

                    pairwise_comparisons[(option1, option2, criterion)] = normalized_diff
                    pairwise_comparisons[(option2, option1, criterion)] = -normalized_diff
        return pairwise_comparisons

    def perform_computation(self, data, pairwise_comparisons):
        scores = pd.DataFrame(index=data.index, columns=data.columns)
        n, m = data.shape
        for criterion in data.columns:
            A = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    if i != j:
                        A[i, j] = pairwise_comparisons[(data.index[i], data.index[j], criterion)]
            eigenvalues, eigenvectors = np.linalg.eig(A)
            max_index = np.argmax(eigenvalues.real)
            _scores = eigenvectors[:, max_index].real
            score_range = _scores.max() - _scores.min()
            if score_range == 0:
                scores[criterion] = [100] * n  # 如果所有分数相同，给予满分
            else:
                normalized_scores = (_scores - _scores.min()) / score_range * 100
                scores[criterion] = normalized_scores
        return scores

    def execute(self):
        try:
            elements = {f'E{i}': self.get_keys_by_value(self.criteria_dict, 'element', f'E{i}') for i in range(1, 4)}
            dimensions = {f'D{i}': self.get_keys_by_value(self.criteria_dict, 'dimension', f'D{i}') for i in
                          range(1, 4)}
            # 创建结果列表
            result = []

            obj_list = self.filter_warehouses(list(self.filled_df.index))
            for obj, _name in obj_list.items():
                _data = self.filled_df.loc[_name]
                min_vals = _data.min()
                max_vals = _data.max()
                range_vals = max_vals - min_vals
                # Prevent normalization errors, If a column's data range is 0, keep the original value
                for column in _data.columns:
                    if range_vals[column] != 0:
                        _data[column] = (_data[column] - min_vals[column]) / range_vals[column]

                pairwise_comparisons = self.preprocess_data(_data)
                scores = self.perform_computation(_data, pairwise_comparisons)
                _weights = self.weights.loc[_name]
                # 维度层
                for i in ['D1', 'D2', 'D3']:
                    set_D = set(dimensions[i])
                    for j in ['E1', 'E2', 'E3']:
                        set_E = set(elements[j])
                        common = list(set_E.intersection(set_D))
                        if common:
                            dim_scores = (scores[common] * _weights[common]).sum(axis=1)
                            df_reset = dim_scores.reset_index()
                            df_reset.columns = ['name_year', 'score']
                            # 分割name_year列
                            df_reset[['name', 'year']] = df_reset['name_year'].str.rsplit('_', n=1, expand=True)
                            # 对数据进行分组处理
                            for name, group in df_reset.groupby('name'):
                                period_values = group.set_index('year')['score'].to_dict()
                                result.append({
                                    "id": name,
                                    "area": self.ids_area[name],
                                    "type": "维度评估",
                                    "dimension": i,
                                    'element': j,
                                    "period_values": period_values
                                })
                # 要素层
                for i in ['E1', 'E2', 'E3']:
                    common = elements[i]
                    if common:
                        dim_scores = (scores[common] * _weights[common]).sum(axis=1)
                        df_reset = dim_scores.reset_index()
                        df_reset.columns = ['name_year', 'score']
                        # 分割name_year列
                        df_reset[['name', 'year']] = df_reset['name_year'].str.rsplit('_', n=1, expand=True)
                        # 对数据进行分组处理
                        for name, group in df_reset.groupby('name'):
                            period_values = group.set_index('year')['score'].to_dict()
                            result.append({
                                "id": name,
                                "area": self.ids_area[name],
                                "type": "要素评估",
                                'element': j,
                                "period_values": period_values
                            })

                # 计算综合权重
                overall_scores = (scores * _weights).sum(axis=1)
                # 重命名列
                df_reset = overall_scores.reset_index()
                df_reset.columns = ['name_year', 'score']
                # 分割name_year列
                df_reset[['name', 'year']] = df_reset['name_year'].str.rsplit('_', n=1, expand=True)
                # 对数据进行分组处理
                for name, group in df_reset.groupby('name'):
                    period_values = group.set_index('year')['score'].to_dict()
                    result.append({
                        "id": name,
                        "area": self.ids_area[name],
                        "type": "综合评估",
                        "period_values": period_values
                    })
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
    def filter_warehouses(warehouse_list):
        # 使用defaultdict来组织数据
        warehouses = defaultdict(list)

        # 遍历列表,将相同储备库的不同年份项目组合在一起
        for item in warehouse_list:
            # 使用正则表达式分离储备库名称和年份
            match = re.match(r'(.+)_(\d{4})$', item)
            if match:
                name, year = match.groups()
                warehouses[name].append(item)

        # 筛选出至少有两个不同年份的储备库
        result = {name: years for name, years in warehouses.items() if len(years) >= 2}

        return result