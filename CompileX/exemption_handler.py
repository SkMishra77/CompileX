from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from utils.responseUtils import res_fun


def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        response = res_fun(0, exc.detail, status_code=exc.status_code)
        return response

    if hasattr(exc, 'args') and exc.args:
        response = res_fun(0, exc.args[0])

    return response
