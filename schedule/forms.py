from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "content")
        labels ={
            'name': 'Enter your name:',
            'content': 'Enter a comment:',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "content": forms.TextInput(attrs={"class": "form-control"}),
        }