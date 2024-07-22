from typing import Any, Dict, List, Optional, Union

from rest_framework import status
from rest_framework.views import Response


def get_response(
    data: Union[Dict[str, Any], List[Any]] = {},
    errors: Union[Dict[str, Any], List[Any]] = {},
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    additional_meta: Optional[Dict[str, Any]] = None
) -> Response:
    """HOW TO USE:
        - data (dict or list): A dictionary or list containing the main response data. Defaults to an empty dict.
        - errors (dict or list): A dictionary or list containing error messages, if any. Defaults to an empty dict.
        - status_code (int): The HTTP status code for the response. Defaults to 500.
        - additional_meta (Optional[Dict[str, Any]]): Additional metadata to include in the response. Defaults to None.

    Example usage:
        - data = {"user": "John Doe"}
        - errors = {"email": "Invalid email format"}
        - status_code = status.HTTP_400_BAD_REQUEST

        return get_response(data=data, errors=errors, status_code=status_code)"""

    response_data = {
        "data": data,
        "errors": errors,
        'meta': {
            'paginator': {
                'next': None,
                'prev': None,
                'page_size': None,
                'count': None,
                'pages': None,
                'current_page': None,
            }
        }
    }

    if additional_meta:
        response_data["meta"].update(additional_meta)

    return Response(response_data, status=status_code)


def get_pagination_response(
    request,
    serializer,
    pagination_class,
    data: Union[Dict[str, Any], List[Any]] = {},
    errors: Union[Dict[str, Any], List[Any]] = {},
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
) -> Response:
    """
    Generate a paginated response for API endpoints.

    Parameters:
    - request: The HTTP request object, used for pagination.
    - serializer: The serializer class used to convert the data into JSON format.
    - pagination_class: The pagination class to be used for paginating the data.
    - data: A dictionary or list of objects to be paginated and serialized (default: {}).
    - errors: A dictionary or list of error messages (default: {}).
    - status_code: The HTTP status code for the response (default: 500 INTERNAL SERVER ERROR).

    Returns:
    A paginated response containing the serialized data.

    Example usage:
        get_pagination_response(
            request=request,
            data=queryset,
            errors={},
            serializer=UserSerializer,
            pagination_class=CustomPaginationClass,
            status_code=status.HTTP_200_OK
        )
    """
    paginator = pagination_class()
    paginated_data = paginator.paginate_queryset(data, request)
    serialized_data = serializer(paginated_data, many=True).data

    return paginator.get_paginated_response(
        data=serialized_data,
        errors=errors,
        status_code=status_code
    )
