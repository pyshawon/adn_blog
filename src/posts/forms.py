from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostCreateForm(forms.ModelForm):
    """
    Post Create Form
    """
    class Meta:
        model = Post
        exclude = ('user', 'slug', 'timestamp',)

