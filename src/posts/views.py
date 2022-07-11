from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import CommentCreateForm
from .models import Post
from .forms import PostCreateForm


# Create your views here.


class PostListView(ListView):
	"""
	Post List View. Paginate By 5 Post
	"""
	model = Post
	template_name = "posts/post_list.html"
	paginate_by = 5
	context_object_name = "posts"


class PostDetails(DetailView):
	"""
	Post Details View. slug is used as a unique identifier.
	"""
	model = Post
	template_name = "posts/post_details.html"
	context_object_name = "post" 
	slug_field = 'slug'
	slug_url_kwarg = 'slug'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetails, self).get_context_data(*args, **kwargs)
		# Load Comment form in Post details page.
		context['comment_form'] = CommentCreateForm()
		return context

	def post(self, request, *args, **kwargs):
		# Save Comment form POST in post details page.
		if not self.request.user.is_authenticated:
			return redirect("/")

		self.object = self.get_object()
		context = super(PostDetails, self).get_context_data(*args, **kwargs)
		comment_form = CommentCreateForm(request.POST)
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.user = self.request.user
			comment.post = self.object
			comment.save()
			context['comment_form'] = CommentCreateForm()
		else:
			context['comment_form'] = comment_form

		return render(request, self.template_name, context)



class PostCreateView(LoginRequiredMixin, CreateView):
	"""
	Post Create View
	"""
	model = Post
	form_class = PostCreateForm
	template_name = "posts/post_create.html"
	success_url = "/"

	def form_valid(self, form):
		# If the form is valid set user to current user in post object.
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


class PostDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Post Delete View
	"""
	model = Post
	template_name = "posts/post_confirm_delete.html"

	def get_queryset(self):
		# Query by current user.
		return self.model.objects.filter(user=self.request.user)

	def form_valid(self, form):
		# If the form is valid delete post object.
		success_url = "/"
		self.object.delete()
		return HttpResponseRedirect(success_url)
