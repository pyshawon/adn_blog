from django.test import TestCase, Client
from users.models import User
from posts.models import Post
from comments.models import Comment
# Create your tests here.


class CommentTestCase(TestCase):
	"""
	Test Case for Blog Post Comments.
	"""
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(
			email="pyshawon.test@gmail.com",
			password="admin@123",
			is_active=True
		)
		self.user1 = User.objects.create_user(
			email="pyshawon.test1@gmail.com",
			password="admin@123",
			is_active=True
		)
		self.client.login(email='pyshawon.test@gmail.com', password='admin@123')
		
		self.post = Post.objects.create(
			user = self.user,
			title = "test post title",
			content = "test post content"
		)


	def test_comment_model(self):
		"""
		Test comment model with .create() method
		"""
		comment = Comment.objects.create(
			post = self.post,
			user = self.user,
			content = "test post comment content"
		)
		self.assertEqual(comment.user, self.user)
		self.assertEqual(comment.post, self.post)
		self.assertEqual(comment.content, "test post comment content")


	def test_comment_model_with_client(self):
		"""
		Test comment model with client http request.
		"""
		data = {
			"post":self.post,
			"user":self.user,
			"content":"test post comment content"
		}
		response = self.client.post(f"/post/{self.post.slug}/", data)

		comment = Comment.objects.last()

		self.assertEqual(response.status_code, 200)

		self.assertEqual(comment.user, self.user)
		self.assertEqual(comment.post, self.post)
		self.assertEqual(comment.content, "test post comment content")


	def test_comment_delete_with_wrong_user(self):
		"""
		Test Comment delete with wrong user.
		"""
		data = {}

		comment = Comment.objects.create(
			post = self.post,
			user = self.user1,
			content = "test post comment content"
		)
		response = self.client.post(f"/comment/{comment.id}/delete/", data)

		self.assertEqual(response.status_code, 404)

	def test_comment_contest_more_then_500_char(self):
		"""
		Test comment content more then 500 char.
		"""
		data = {
			"post":self.post,
			"user":self.user,
			"content":"test post comment content" * 100
		}
		response = self.client.post(f"/post/{self.post.slug}/", data)

		comment = Comment.objects.last()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(comment, None)

