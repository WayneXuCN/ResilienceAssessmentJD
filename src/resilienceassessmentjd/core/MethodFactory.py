# !/usr/bin/env python
# @FileName  :MethodFactory.py
# @Time      :2024/5/16 下午2:05
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

from ..methods.AHP import AHP
from ..methods.DEMATEL import DEMATEL
from ..methods.EWM import EWM
from ..methods.HEWM import HEWM
from ..methods.MACBETH import MACBETH
from ..methods.MEE import MEE
from ..methods.PCA import PCA
from ..methods.VIKOR import VIKOR
from .ScalingMethod import BenchmarkRatioNormalization, MinMaxNormalization


class DecisionMethodFactory:
    """
    A factory class for creating decision method instances.

    This class uses a registration system to map method names to corresponding decision method classes.
    It allows for dynamic addition and retrieval of decision methods based on method names.

    Attributes
    ----------
    _methods : dict
        A private dictionary that maps method names (str) to decision method classes.

    Methods
    -------
    register_method(method_name, method_class)
        Registers a decision method class under the specified method name.

    get_method(method_name, params)
        Retrieves an instance of the specified decision method class,
        initialized with the given parameters.
    """

    _methods = {}

    @classmethod
    def register_method(cls, method_name, method_class):
        """
        Register a decision method class under a specific name.

        Parameters
        ----------
        method_name : str
            The name under which the decision method class is to be registered.
        method_class : DecisionMethod
            The class to be registered for the decision method.

        """
        cls._methods[method_name] = method_class
        print(f"Registered decision method: {method_name}")

    @classmethod
    def get_method(cls, method_name, params):
        """
        Retrieve an instance of a registered decision method class, initialized with the specified parameters.

        Parameters
        ----------
        method_name : str
            The name of the decision method to retrieve.
        params : dict
            The parameters for initializing the decision method instance.

        Returns
        -------
        instance : DecisionMethod
            An instance of the decision method initialized with the specified parameters.

        Raises
        ------
        ValueError
            If the method name is not registered in the factory.

        """
        if method_name in cls._methods:
            return cls._methods[method_name](params)
        else:
            raise ValueError(f"Unknown decision method: {method_name}")


def register_decision_method(method_class):
    """
    Decorator to register a decision method class in the DecisionMethodFactory.

    This function is designed as a decorator that can be used to register decision method
    classes directly without calling the `register_method` of the factory class explicitly.

    Parameters
    ----------
    method_class : DecisionMethod
        The decision method class to register. This class should be a subclass of DecisionMethod
        and must implement all the required methods and properties defined in DecisionMethod.

    Returns
    -------
    method_class : DecisionMethod
        The same class that was passed in. This is returned to allow the class to be used
        normally even after being decorated.

    Examples
    --------
    >>> @register_decision_method
    ... class _AHP(DecisionMethod):
    ...     pass
    ...
    >>> # AHP is now registered in the factory under the name 'AHP'
    """
    DecisionMethodFactory.register_method(method_class.__name__, method_class)
    return method_class


class ScalingMethodFactory:
    """
    A factory class for creating scaling method instances.

    This class uses a registration system to map method names to corresponding scaling method classes.
    It allows for dynamic addition and retrieval of scaling methods based on method names.

    Attributes
    ----------
    _methods : dict
        A private dictionary that maps method names (str) to scaling method classes.

    Methods
    -------
    register_method(method_name, method_class)
        Registers a scaling method class under the specified method name.

    get_method(method_name, params)
        Retrieves an instance of the specified scaling method class,
        initialized with the given parameters.
    """

    _methods = {}

    @classmethod
    def register_method(cls, method_name, method_class):
        """
        Register a scaling method class under a specific name.

        Parameters
        ----------
        method_name : str
            The name under which the scaling method class is to be registered.
        method_class : ScalingMethod
            The class to be registered for the scaling method.

        """
        cls._methods[method_name] = method_class
        print(f"Registered scaling method: {method_name}")

    @classmethod
    def get_method(cls, method_name, params):
        """
        Retrieve an instance of a registered scaling method class, initialized with the specified parameters.

        Parameters
        ----------
        method_name : str
            The name of the scaling method to retrieve.
        params : dict or dataframe
            A dictionary of parameters for initializing the scaling method instance.

        Returns
        -------
        instance : ScalingMethod
            An instance of the scaling method initialized with the specified parameters.

        Raises
        ------
        ValueError
            If the method name is not registered in the factory.

        """
        if method_name in cls._methods:
            return cls._methods[method_name](params)
        else:
            raise ValueError(f"Unknown data scaling method: {method_name}")


def register_scaling_method(method_class):
    """
    Decorator to register a scaling method class in the ScalingMethodFactory.

    This function is designed as a decorator that can be used to register scaling method
    classes directly without calling the `register_method` of the factory class explicitly.

    Parameters
    ----------
    method_class : ScalingMethod
        The scaling method class to register. This class should be a subclass of ScalingMethod
        and must implement all the required methods and properties defined in ScalingMethod.

    Returns
    -------
    method_class : ScalingMethod
        The same class that was passed in. This is returned to allow the class to be used
        normally even after being decorated.

    Examples
    --------
    >>> @register_scaling_method
    ... class _MinMaxNormalization(ScalingMethod):
    ...     pass
    ...
    >>> # MinMaxNormalization is now registered in the factory under the name 'MinMaxNormalization'
    """
    ScalingMethodFactory.register_method(method_class.__name__, method_class)
    return method_class


# Register decision methods in the DecisionMethodFactory
DecisionMethodFactory.register_method("HEWM", HEWM)
DecisionMethodFactory.register_method("AHP", AHP)
DecisionMethodFactory.register_method("DEMATEL", DEMATEL)
DecisionMethodFactory.register_method("EWM", EWM)
DecisionMethodFactory.register_method("PCA", PCA)
DecisionMethodFactory.register_method("MEE", MEE)
DecisionMethodFactory.register_method("VIKOR", VIKOR)
DecisionMethodFactory.register_method("MACBETH", MACBETH)

# Register scaling methods in the ScalingMethodFactory
ScalingMethodFactory.register_method("MinMax", MinMaxNormalization)
ScalingMethodFactory.register_method("BRM", BenchmarkRatioNormalization)
