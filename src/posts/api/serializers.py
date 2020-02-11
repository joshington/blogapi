from rest_framework.serializers import  (
		Modelserializer, HyperLinkedIdentityField,SerializerMethodField
	)

from comments.api.serializers import CommentSerializer
from posts.models import Post

class PostCreateSerializer(Modelserializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]
class PostListSerializer(Modelserializer):
	url = post_detail_url
	user = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			#'slug',===slug not needed anymore since i have it in the lookup_field
			'content',
			'publish',
		]

	def get_user(self,obj):
		return str(obj.user.username)
#we use this when we are trying to get the username of the logged  in user

class PostListSerializer(Modelserializer):
	url = post_detail_url
	class Meta:
		model = Post
		fields = [
			'title',
			'slug',
			'content',
			'publish',

		]

post_detail_url = HyperLinkedIdentityField(
			view_name='posts-api:detail',#linking my post
			lookup_field='slug',#by defuallt the lookup field is usually the primary key
		)
class PostDetailSerializer(Modelserializer):
	url=post_detail_url
	user= SerializerMethodField()
	image  = SerializerMethodField()
	markdown = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'title',
			'slug',
			'content',
			'markdown',
			'publish',
			'user',
			'image',

		]

	def get_markdown():
		return obj.get_markdown()
	def get_user(self,obj):
		return str(obj.user.username)

	def get_image(self,obj):
		try:
			image = obj.image.url#gives us the url of the image if the image exist
		except:
			image = None
		return image
"""

#data is supposed to return serialized data
data = {
	"title":"Yeah buddy",
	"content":"New content",
	"publish":"2016-2-12",
	"slug":"Yeah-buddy"
}
new_item = PostSerializer(data=data)
if  new_item.is_valid():
	new_item.save()
else:
	print(new_item.errors)
"""
