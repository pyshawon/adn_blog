from django.shortcuts import render
from .models import Comment
from .forms import CommentCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

# Create your views here.



class CommentDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Delete Comment if the comment posted by current users.
	"""
	model = Comment
	template_name = "comments/comment_confirm_delete.html"

	def get_queryset(self):
		# Query only for current user data.
		return self.model.objects.filter(user=self.request.user)

	def form_valid(self, form):
		success_url = self.object.post.get_absolute_url()
		self.object.delete()
		return HttpResponseRedirect(success_url)