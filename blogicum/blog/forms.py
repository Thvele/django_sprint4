from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'created_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'rows': 3,
                       'placeholder': 'Введите ваш комментарий...'}),
        }
        labels = {'text': ''}
