from rest_framework.serializers import  (
		Modelserializer, HyperLinkedIdentityField,SerializerMethodField
	)

from comments.models import Comment


class CommentSerializer(Modelserializer):
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'parent ',
			'content',
			'reply_count',
			'timestamp',
		]
	def get_reply_count():
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentChildSerializer(Modelserializer):
	class Meta:
		model = Comment
		fields = [
			'id',
			'content',
			'timestamp',
		]

class CommentDetailSerializer(Modelserializer):
	replies =  SerializerMethodField()#the replies are the children
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'replies',
			'timestamp',
		]
#====kinda tricky on this not getting it properly======
	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_reply_count():
		if obj.is_parent:
			return obj.children().count()
		return 0