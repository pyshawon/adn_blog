from django.db import models
from posts.models import Post
from django.conf import settings
# Create your models here.


class Comment(models.Model):
	"""
	Comment Model.
	User can be null of user is deleted
	"""
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.id)
		
	def get_user(self):
		"""
		Get full name of the user if post user is not
		deleted or show Deleted user
		"""
		return self.user.get_name() if self.user else "Deleted user"