# !/usr/bin/env python
# @FileName  :UnifiedModel.py
# @Time      :2024/5/16 下午2:03
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

from .Criterion import Criterion
from .ExceptionHandler import BusinessException
from .MethodFactory import DecisionMethodFactory, ScalingMethodFactory


class UnifiedModel:
    """
    A unified model for resilience assessment using different methods.

    Parameters:
    -----------
    request : dict
        The JSON request containing the method and parameters for resilience assessment.
    """

    def __init__(self, request):
        """Initialize the unified model with a JSON request."""
        self.request = request
        self.assess_type = request.get("assess_type", "")
        self.assess_method = request.get("assess_method", "")
        self.weights = None
        # Get the processed params
        create_criteria = Criterion(request)
        self.params = create_criteria.get_criteria()

    def execute(self):
        """
        Execute the unified model to perform resilience assessment.
        """
        try:
            weights = self.determine_weight()  # Determine the weights
            if weights["status"] == "success":
                self.params["weights"] = weights[
                    "weights"
                ]  # Add the weights to the parameters
            else:
                raise BusinessException("Failed to calculate weights.")
            normalized_data = self.scaling_data()  # Scale the data
            if normalized_data["status"] == "success":
                self.params["norm_data"] = normalized_data[
                    "data"
                ]  # Add the normalized data to the parameters
            method_instance = DecisionMethodFactory.get_method(
                self.request.get("assess_method"), self.params
            )
            # Get the method instance
            results = method_instance.execute()  # Execute the method
            return {
                "status": "0",
                "message": "success",
                "assess_type": self.assess_type,
                "results": results,  # Format the output
            }
        except Exception as e:
            return {
                "status": "1",
                "message": f"Exception information: {str(e)}",
            }

    def determine_weight(self):
        """
        Determine the weights for the resilience assessment.
        """
        weight_method = self.request.get("weight_method", {})
        subjective_method = weight_method.get("subjective_method", {})
        objective_method = weight_method.get("objective_method", {})
        combined_method = weight_method.get("combined_method", {})

        # If all three methods are provided, return the combined weights
        if subjective_method and objective_method and combined_method:
            # Execute the subjective and objective methods to get the weights
            subj_weights = DecisionMethodFactory.get_method(
                subjective_method, self.params
            ).execute()
            obj_weights = DecisionMethodFactory.get_method(
                objective_method, self.params
            ).execute()
            combined_params = {
                "subjective_weights": subj_weights,
                "objective_weights": obj_weights,
            }
            self.params["combined_params"] = combined_params
            combined_instance = DecisionMethodFactory.get_method(
                combined_method, self.params
            )
            combined_weights = combined_instance.execute()
            return combined_weights

        # If only the subjective method is provided, return the subjective weights
        elif subjective_method:
            return DecisionMethodFactory.get_method(
                subjective_method, self.params
            ).execute()
        # If only the objective method is provided, return the objective weights
        elif objective_method:
            return DecisionMethodFactory.get_method(
                objective_method, self.params
            ).execute()
        # If any valid weight determination method is provided, return the ValueError
        else:
            raise BusinessException("No valid weight determination method provided.")

    def scaling_data(self):
        """
        Scale the data for resilience assessment.
        """
        scaling_method = self.request.get("normalization", "MinMax")
        if scaling_method:
            return ScalingMethodFactory.get_method(
                scaling_method, self.params
            ).execute()
        else:
            raise BusinessException("No valid data scaling method provided.")
