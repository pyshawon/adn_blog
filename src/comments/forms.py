from django import forms
from django.core.exceptions import ValidationError
from .models import Comment

class CommentCreateForm(forms.ModelForm):
    """
    Comment Create Form.
    """
    class Meta:
        model = Comment
        exclude = ('post', 'user', 'timestamp',)

    def clean_content(self):
        """
        Check the comment is not blank and > 500 char.
        """
        data = self.cleaned_data['content']
        if not data:
            raise forms.ValidationError("Please enter your content")

        if len(data) > 500:
            raise forms.ValidationError("Comment Should be less than 500 characters ")

        return data


