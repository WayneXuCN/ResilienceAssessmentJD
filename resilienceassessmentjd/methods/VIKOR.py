# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :VIKOR.py
# @Time      :2024/7/2 下午7:39
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import traceback

import numpy as np
import pandas as pd

from ..core.DecisionMethod import DecisionMethod


# from ..core.ExceptionHandler import *


class VIKOR(DecisionMethod):
    """
    VIKOR Model.

    This class implements the VIKOR Model for decision-making.
    """

    def __init__(self, params):
        super().__init__(params)

    def preprocess_data(self):
        # %%
        weights = pd.DataFrame(self.params["weights"].copy(), columns=self.params['criteria_names'],
                               index=self.params["ids_area"].keys())
        ids_area = self.params["ids_area"]
        criteria_dict = self.params['criteria_dict']
        criteria_types = {key: value.get('attribute') for key, value in criteria_dict.items()}
        # For negative indicators (type 1), a 1-x conversion is required
        for key, value in criteria_types.items():
            if value == '1':
                self.filled_df[key] = 1 - self.filled_df[key]
        return weights, ids_area, criteria_dict, criteria_types

    def perform_computation(self, norm_data, criteria_types, weights):
        """
        Perform the specific computation for the decision method.

        This method should be implemented by each subclass to perform the calculation or
        operation specific to the decision method.

        Returns
        -------
        result : any
            The result of the computation.

        Raises
        ------
        NotImplementedError
            If a subclass does not implement this method.
        """
        try:
            # Calculate ideal solution and negative ideal solution
            f_star = norm_data.max()
            f_minus = norm_data.min()

            # For a 0/1 variable, if all values are the same, set f _ star and f _ minus to the same value to avoid dividing by zero
            for col, criteria_type in zip(norm_data.columns, criteria_types):
                if criteria_type == 2 and f_star[col] == f_minus[col]:
                    f_star[col] = f_minus[col] = 1

                # Calculate S and R
            S = np.zeros(len(norm_data))
            R = np.zeros(len(norm_data))

            for i, (_, row) in enumerate(norm_data.iterrows()):
                s_values = weights.iloc[i] * (f_star - row) / (f_star - f_minus)
                S[i] = s_values.sum()
                R[i] = s_values.max()

            # Calculate Q
            v = 0.5  # Strategy weight, usually 0.5
            S_star, S_minus = min(S), max(S)
            R_star, R_minus = min(R), max(R)

            # Avoid dividing by zero
            S_range = S_minus - S_star
            R_range = R_minus - R_star
            S_term = (S - S_star) / S_range if S_range != 0 else np.zeros_like(S)
            R_term = (R - R_star) / R_range if R_range != 0 else np.zeros_like(R)
            Q = v * S_term + (1 - v) * R_term

            # 计算RI值
            RI = 1 - Q

            VIKOR_results = pd.DataFrame({
                'S': S,
                'R': R,
                'Q': Q,
                'RI': RI  # 添加RI列
            }, index=norm_data.index)

            # Sort by Q value (smaller is better)
            # VIKOR_results = VIKOR_results.sort_values('Q')
            # Sort by RI value (bigger is better)
            VIKOR_results = VIKOR_results.sort_values('RI', ascending=False)
            return VIKOR_results
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())

    def execute(self):
        try:
            weights, ids_area, criteria_dict, criteria_types = self.preprocess_data()
            result = []
            norm_df = self.filled_df.div(self.filled_df.abs().sum(axis=0), axis=1)
            comprehensive_results = self.perform_computation(norm_df, criteria_types, weights)
            for _id, area in ids_area.items():
                if _id in self.params['invalid_ids']:
                    score = {
                        'id': _id,
                        'area': area,
                        'type': '综合评估',
                        'index_value': '/',
                        'level': '/'
                    }
                else:
                    score = {
                        'id': _id,
                        'area': area,
                        'type': '综合评估',
                        'index_value': comprehensive_results.loc[_id, 'RI'],
                        'level': comprehensive_results.index.get_loc(_id) + 1
                    }
                result.append(score)

            elements = {f'E{i}': self.get_keys_by_value(criteria_dict, 'element', f'E{i}') for i in range(1, 4)}
            dimensions = {f'D{i}': self.get_keys_by_value(criteria_dict, 'dimension', f'D{i}') for i in range(1, 4)}

            for e, criteria in elements.items():
                if not criteria:  # 跳过空的维度
                    continue
                # 提取该维度的相关数据
                ele_decision_matrix = norm_df[criteria]
                ele_weights_matrix = weights[criteria]
                ele_criteria_types = {c: criteria_types[c] for c in criteria}
                ele_results = self.perform_computation(ele_decision_matrix, ele_criteria_types, ele_weights_matrix)
                for _id, area in ids_area.items():
                    if _id in self.params['invalid_ids']:
                        score = {
                            'id': _id,
                            'area': area,
                            'type': '要素评估',
                            'element': e,
                            'index_value': '/',
                            'level': '/'
                        }
                    else:
                        score = {
                            'id': _id,
                            'area': area,
                            'type': '要素评估',
                            'element': e,
                            'index_value': ele_results.loc[_id, 'RI'],
                            'level': ele_results.index.get_loc(_id) + 1
                        }
                    result.append(score)

            dim_ele_list = {f'D{i}': {f'E{j}': [] for j in range(1, 4)} for i in range(1, 4)}

            for key, value in criteria_dict.items():
                dimension = value['dimension']
                element = value['element']
                dim_ele_list[dimension][element].append(key)

            for dim, dim_dict in dim_ele_list.items():
                for ele, c in dim_dict.items():
                    if not c:  # 跳过空的维度
                        continue
                        # 提取该维度的相关数据
                    dim_decision_matrix = norm_df[c]
                    dim_weights_matrix = weights[c]
                    dim_criteria_types = {ind: criteria_types[ind] for ind in c}
                    # 对该维度进行VIKOR分析
                    dim_results = self.perform_computation(dim_decision_matrix, dim_criteria_types, dim_weights_matrix)
                    for _id, area in ids_area.items():
                        if _id in self.params['invalid_ids']:
                            score = {
                                'id': _id,
                                'area': area,
                                'type': '维度评估',
                                'dimension': dim,
                                'element': ele,
                                'index_value': '/',
                                'level': '/'
                            }
                        else:
                            score = {
                                'id': _id,
                                'area': area,
                                'type': '维度评估',
                                'dimension': dim,
                                'element': ele,
                                'index_value': dim_results.loc[_id, 'RI'],
                                'level': dim_results.index.get_loc(_id) + 1
                            }
                        result.append(score)
            return result
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())

    @staticmethod
    def get_keys_by_value(d, value_key, target_value):
        return [k for k, v in d.items() if v[value_key] == target_value]
