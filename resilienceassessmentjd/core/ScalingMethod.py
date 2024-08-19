# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ScalingMethod.py
# @Time      :2024/6/1 下午8:41
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

# from .ExceptionHandler import *
import traceback

import pandas as pd


class ScalingMethod:
    """
    Base class for all scaling methods.

    This class provides a template for creating new scaling methods. All scaling method
    classes should inherit from this class and implement the execute method
    according to their specific requirements.

    Methods
    -------
    execute(self):
        Executes the specific computation of the scaling method. This method must be
        overridden by subclasses.

    Examples
    --------
    >>> class SampleScalingMethod(ScalingMethod):
    ...     def execute(self):
    ...         # Implementation specific to SampleScalingMethod
    ...         pass
    >>> # SampleScalingMethod should implement all abstract methods
    --------
    """

    def __init__(self, params):
        """
        Initializes the scaling method with parameters.

        Parameters
        ----------
        params : dict
            The parameters for initializing the decision method instance.

        Raises
        ------
        ValueError
            If the parameters provided are invalid.
        """
        self.params = params
        self.df = params.get("init_data")
        self.filled_df = params.get("filled_data")
        self.norm_df = params.get("norm_data")

    def execute(self):
        """
        Execute the specific computation for the scaling method.

        This method should be implemented by each subclass to perform the scaling or
        normalization specific to the scaling method.

        Returns
        -------
        result : pd.DataFrame
            The result of the scaling method execution.

        Raises
        ------
        NotImplementedError
            If a subclass does not implement this method.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")


class MinMaxNormalization(ScalingMethod):
    def __init__(self, params):
        super().__init__(params)

    def execute(self):
        """
        Perform Min-Max normalization on the data.

        Returns
        -------
        normalized_data : pd.DataFrame
            The normalized data using Min-Max normalization.
        """
        try:
            min_vals = self.df.min()
            max_vals = self.df.max()
            range_vals = max_vals - min_vals

            # Prevent normalization errors, If a column's data range is 0, keep the original value
            normalized_data = self.df.copy()
            for column in self.df.columns:
                if range_vals[column] != 0:
                    normalized_data[column] = (self.df[column] - min_vals[column]) / range_vals[column]

            return {"status": "success", "data": normalized_data}

        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())


class ZScoreNormalization(ScalingMethod):
    def __init__(self, params):
        super().__init__(params)

    def execute(self):
        """
        Perform Z-Score normalization on the data.

        Returns
        -------
        normalized_data : pd.DataFrame
            The normalized data using Z-Score normalization.
        """
        try:
            mean_vals = self.df.mean()
            std_vals = self.df.std()
            # Prevent normalization errors when the standard deviation is 0
            normalized_data = self.df.copy()
            for column in self.df.columns:
                if std_vals[column] != 0:
                    normalized_data[column] = (self.df[column] - mean_vals[column]) / std_vals[column]
                else:
                    # When the standard deviation is 0, keep the original value
                    normalized_data[column] = self.df[column]

            return {"status": "success", "data": normalized_data}

        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())


class BenchmarkRatioNormalization(ScalingMethod):
    def __init__(self, params):
        super().__init__(params)

    def execute(self):
        """
        Perform Min-Max normalization on the data.

        Returns
        -------
        normalized_data : pd.DataFrame
            The normalized data using Min-Max normalization.
        """
        try:
            min_vals = self.df.min()
            max_vals = self.df.max()
            range_vals = max_vals - min_vals

            # Prevent normalization errors, If a column's data range is 0, keep the original value
            normalized_data = self.df.copy()
            for column in self.df.columns:
                if range_vals[column] != 0:
                    normalized_data[column] = (self.df[column] - min_vals[column]) / range_vals[column]

            return {"status": "success", "data": normalized_data}

        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())
