from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    title = forms.CharField(
        label='Title',
        max_length=200,
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "title",
            "type": "text",
            "placeholder": "Enter the title here",
            "data-sb-validations": "required"
        })
    )

    sommary=forms.CharField(
        label='Sommary',
        max_length=250,
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "sommary",
            "type": "text",
            "placeholder": "Enter the sommary here",
            "data-sb-validations": "required"
        })
    )

    body = forms.CharField(
        label='Body',
        help_text='',
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "id": "body",
            "type": "text",
            "placeholder": "Enter the content here",
            'style': 'height: 150px;',
            "data-sb-validations": "required"
        })
    )
    

    class Meta:
        model = Post
        fields = ('title','sommary','body')

