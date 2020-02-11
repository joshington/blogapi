 from django.db.models import Q #handling the Q lookup

from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,
	)
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	DestroyAPIView
	) #want to list the posts

#pagination is neing handled right here

#handling permissions here
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
)
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination,PostPageNumberPagination


from commects.models import Comment 



from .serializers import (
	CommentSerializer,
	CommentDetailSerializer,
	)
#class PostCreateAPIView(CreateAPIView):
#

class CommentListAPIView(ListAPIView):
	#queryset = Post.objects.all()
	serializer_class = CommentSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields   = ['content', 'user__first_name']#user can only be able to check those
	pagination_class = PostPageNumberPagination#PostLimitOffsetPagination

	#we intend to override our get_queryset method
	def get_queryset(self, *args, **kwargs):
		#queryset_list  = Post.objects.filter(user=self.request.user)==could use that if maybe its GET
		queryset_list = Comment.objects.all()
		#orqueryset_lst = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		#similar to the above
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list

class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	lookup_field = 'pk'
	#lookup_field_kwarg = "abc"#fixes the slug to abc


#