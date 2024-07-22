from math import ceil
from typing import Any, Dict, List, Union

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Paginator(PageNumberPagination):
    """Digipactum standard paginated response."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 9000
    page_query_param = 'page'

    def get_paginated_response(
        self,
        data: Union[Dict[str, Any], List[Any]] = {},
        errors: Union[Dict[str, Any], List[Any]] = {},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> Response:
        total_items = self.page.paginator.count
        current_page_size = self.get_page_size(self.request)
        total_pages = ceil(total_items / current_page_size)

        return Response({
            'data': data,
            'errors': errors,
            'meta': {
                'paginator': {
                    'next': self.get_next_link(),
                    'prev': self.get_previous_link(),
                    'page_size': current_page_size,
                    'count': total_items,
                    'pages': total_pages,
                    'current_page': self.page.number,
                }
            }
        }, status=status_code)
