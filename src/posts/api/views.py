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
from .pagination import PostLimitOffsetPagination,PostPageNumberPagination

#handling permissions here
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
)

from posts.models import Post 

from .permissions import IsOwnerOrReadOnly

from .serializers import (
	PostCreateSerializer, 
	PostListSerializer,
	PostDetailSerializer,
	)
class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
#for user to create apost they must be authenticated
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)#this is gonna use the user field for the Post model


class PostListAPIView(ListAPIView):
	#queryset = Post.objects.all()
	serializer_class = PostSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields   = ['title', 'content', 'user__first_name']#user can only be able to check those
	pagination_class = PostPageNumberPagination#PostLimitOffsetPagination

	#we intend to override our get_queryset method
	def get_queryset(self, *args, **kwargs):
		#queryset_list  = Post.objects.filter(user=self.request.user)==could use that if maybe its GET
		queryset_list = Post.objects.all()
		#orqueryset_lst = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		#similar to the above
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
					Q(title__icontains=query)|
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'
	#lookup_field_kwarg = "abc"#fixes the slug to abc

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]#user should be authenticated or else readonly

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)#this changes the update from the original user that
#have to make sure that the user trying to update the post is the owner of the object
#submitted to this new user.
		#could us use this segment here to notify the logged in user that email was updated
		#so watch those two functions;perform_update and perform_create critically they are useful

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'
	permissions = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]