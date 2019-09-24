from django import forms
from .models import Test, Comment


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'test_text')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
