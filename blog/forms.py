from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Comments, Post


class CreatePost(forms.ModelForm):
    """ModelForm used for creating/editing blog posts."""
    body = forms.CharField(widget=CKEditorWidget(), label='Content')

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'body', 'img_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Post title'}),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Subtitle'}),
            'img_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '/static/assets/img/post-bg.jpg'}),
        }


class UsersComments(forms.ModelForm):
    """Form for adding comments."""
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control',
                   'placeholder': 'Write your comment...'}),
        max_length=2000,
        required=True,
        label='Comment'
    )

    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}),
        }
