from requests import request
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


# class CustomPagination(PageNumberPagination):
#     def get_page_number(self, request, paginator):
#         return int(request.query_params.get('page', 1))

#     def get_page_size(self, request):
#         self.page_size = int(request.query_params.get('limit', 15)) 
#         return int(request.query_params.get('limit', 15))

#     def get_paginated_response(self, data):
#         return Response({
#             'meta': {
#                 'current_page': self.page.number,
#                 'from':  (self.page.number - 1) * self.page_size + 1 if self.page.paginator.count > 0  else 0,
#                 'last_page': self.page.paginator.num_pages,
#                 'per_page': self.page_size,
#                 'to':  self.page.paginator.count if self.page.number * self.page_size > self.page.paginator.count else self.page.number * self.page_size,
#                 'total': self.page.paginator.count
#             },
#             'results': data
#          })
    

# class CustomLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 10
#     max_limit = 100

#     def get_paginated_response(self, data):
#         return Response({
#             'meta': {
#                 'has_more': self.offset + self.limit < self.count,
#             },
#             'results': data
#         })