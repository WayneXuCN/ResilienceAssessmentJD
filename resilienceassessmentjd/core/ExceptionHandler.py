# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ExceptionHandler.py
# @Time      :2024/6/2 下午1:05
# @Author    :Wenjie Xu
# @Email     :wenjie.xu.cn@outlook.com

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorCodes:
    BUSINESS_ERROR = "B1001"
    SYSTEM_ERROR = "S1001"
    UNKNOWN_ERROR = "U1001"


class ExceptionHandler:
    """
    A centralized exception handler for managing errors across the project.
    """

    @staticmethod
    def handle_exception(error, context=""):
        """
        Handle the given exception by logging the error and returning a standardized error response.

        Parameters
        ----------
        error : Exception
            The exception to handle.
        context : str, optional
            Additional context about where the error occurred.

        Returns
        -------
        dict
            A standardized error response containing the error message, status, and code.
        """
        if isinstance(error, BusinessException):
            logger.warning(f"Business error in {context}: {error.message}")
            return {"status": "error", "message": error.message, "code": error.code}

        elif isinstance(error, SystemException):
            logger.error(f"System error in {context}: {error.message}")
            # Send notification to maintenance team
            ExceptionHandler.notify_maintenance_team(error, context)
            return {"status": "error", "message": "System is currently unavailable. Please try again later.",
                    "code": error.code}

        else:
            logger.critical(f"Unexpected error in {context}: {error.message}")
            # Send notification to development team
            ExceptionHandler.notify_development_team(error, context)
            return {"status": "error", "message": "An unexpected error occurred. Please try again later.",
                    "code": error.code}

    @staticmethod
    def notify_maintenance_team(error, context):
        """
        Notify the maintenance team about the system error.

        Parameters
        ----------
        error : Exception
            The exception that occurred.
        context : str
            Additional context about where the error occurred.
        """
        # Implementation to notify the maintenance team (e.g., send an email or a message)
        logger.info(f"Notification sent to maintenance team about system error in {context}: {error.message}")

    @staticmethod
    def notify_development_team(error, context):
        """
        Notify the development team about the unexpected error.

        Parameters
        ----------
        error : Exception
            The exception that occurred.
        context : str
            Additional context about where the error occurred.
        """
        # Implementation to notify the development team (e.g., send an email or a message)
        logger.info(f"Notification sent to development team about unexpected error in {context}: {error.message}")


class BusinessException(Exception):
    """
    Exception raised for business logic errors.
    """

    def __init__(self, message="Business exception occurred", code=ErrorCodes.BUSINESS_ERROR):
        self.message = message
        self.code = code
        super().__init__(self.message)


class SystemException(Exception):
    """
    Exception raised for system-related errors.
    """

    def __init__(self, message="System exception occurred", code=ErrorCodes.SYSTEM_ERROR):
        self.message = message
        self.code = code
        super().__init__(self.message)


class CustomException(Exception):
    """
    Exception raised for other unforeseen errors.
    """

    def __init__(self, message="An unexpected error occurred", code=ErrorCodes.UNKNOWN_ERROR):
        self.message = message
        self.code = code
        super().__init__(self.message)
