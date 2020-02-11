from rest_framework.permissions import BasePermission, SAFE_METHODS

class  IsOwnerOrReadOnly(BasePermission):
	message = "You must be the owner of this object."
	my_safe_method = ['GET','PUT']

	def has_permission(self,request, view):
		#similar to has _object permission, nothing very muc different
		if request.method in self.my_safe_method:
			return True
		return False

	def has_object_permission(self, request,view,obj):
		#member = Membership.objects.get(uer=request.user)
		#member.is_active
		if request.method in SAFE_METHODS
			return True#this will only allow you to update the object if your the owner user
		return obj.user == request.user#making suer that the request user is same as that one who 
#created the object, and the object user is comming from the user in the Post model