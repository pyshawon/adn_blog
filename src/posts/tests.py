from django.test import TestCase, Client
from users.models import User
from posts.models import Post
# Create your tests here.


class PostTestCase(TestCase):
	"""
	Test Case for Blog Posts.
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

	def test_post_model(self):
		"""
		Test post model with .create() method
		"""
		post = Post.objects.create(
			user = self.user,
			title = "test post title",
			content = "test post content"
		)
		self.assertEqual(post.user, self.user)
		self.assertEqual(post.title, "test post title")
		self.assertEqual(post.content, "test post content")

	def test_post_list(self):
		"""
		Test post list/home page response.
		"""
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)

	def test_post_model_with_client(self):
		"""
		Test post model with client http request.
		"""
		data = {
			"user": self.user,
			"title":"test post title",
			"content":"test post content"
		}
		response = self.client.post("/post/create/", data, format="multipart")
		post = Post.objects.last()

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/")

		self.assertEqual(post.user, self.user)
		self.assertEqual(post.title, "test post title")
		self.assertEqual(post.content, "test post content")


	def test_post_delete_with_wrong_user(self):
		"""
		Test post model with wrong user.
		"""
		data = {}

		post = Post.objects.create(
			user = self.user1,
			title = "test post title u1",
			content = "test post content u1"
		)
		response = self.client.post(f"/post/{post.id}/delete/", data)

		self.assertEqual(response.status_code, 404)


	def test_post_delete(self):
		"""
		Test post delete with right user.
		"""
		data = {}

		post = Post.objects.create(
			user = self.user,
			title = "test post title u1",
			content = "test post content u1"
		)
		response = self.client.post(f"/post/{post.id}/delete/", data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/")

