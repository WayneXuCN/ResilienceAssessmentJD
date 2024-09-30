# !/usr/bin/env python
# @FileName  :DecisionMethod.py
# @Time      :2024/5/16 下午2:07
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

# from .ExceptionHandler import *
import traceback


class DecisionMethod:
    """
    Base class for all decision methods.

    This class provides a template for creating new decision methods. All decision method
    classes should inherit from this class and implement the execute method
    according to their specific requirements.

    Methods
    -------
    execute(self):
        Executes the specific computation of the decision method. This method must be
        overridden by subclasses.

    Examples
    --------
    >>> class SampleMethod(DecisionMethod):
    ...     def execute(self):
    ...         # Implementation specific to SampleMethod
    ...         pass
    >>> # SampleMethod should implement all abstract methods
    --------
    """

    def __init__(self, params):
        """
        Initializes the decision method with parameters.

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

    def preprocess_data(self):
        """
        Preprocess the input data if necessary.


        This method can be overridden by subclasses to implement any required data preprocessing steps.
        """
        pass

    def perform_computation(self):
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
        raise NotImplementedError("This method should be overridden by subclasses.")

    def execute(self):
        """
        Execute the specific computation for the decision method.

        This method should be implemented by each subclass to perform the calculation or
        operation specific to the decision method.

        Returns
        -------
        result : dict
            The result of the decision method execution.

        Raises
        ------
        NotImplementedError
            If a subclass does not implement this method.
        """
        try:
            self.preprocess_data()
            result = self.perform_computation()
            return {"status": "success", "result": result}
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}")
            print(f"Exception information: {str(e)}")
            print("Detailed information:")
            print(traceback.format_exc())
