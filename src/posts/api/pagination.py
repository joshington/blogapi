from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)

class PostLimitOffsetPagination(LimitOffsetPagination):
	default_limit = 10#lists to about 10 posts 
	max_limit = 10
	
class PostPageNumberPagination(PageNumberPagination):
	page_size = 2
	