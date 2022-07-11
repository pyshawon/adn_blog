from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
	"""
	Post Model.
	User can be null of user is deleted
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=255)
	slug = models.CharField(max_length=200, unique=True, null=True, blank=True)
	content = models.TextField()
	image = models.ImageField(upload_to="blog_image", null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.title)

	def save(self, *args, **kwargs):
		"""
		Create Post slug when a post create or updated.
		"""
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

	def get_letest_comments(self):
		"""
		Get letest 3 comments for a post to show in the home page
		"""
		return self.comment_set.all()[:3]

	def get_comments(self):
		"""
		Get all. the comment for a post.
		"""
		return self.comment_set.all()

	def get_user(self):
		"""
		Get full name of the user if post user is not
		deleted or show Deleted user
		"""
		return self.user.get_name() if self.user else "Deleted user"

	def get_absolute_url(self):
		"""
		Get URL/PATH of the post.
		"""
		return reverse('post_details', args=[str(self.slug)])
