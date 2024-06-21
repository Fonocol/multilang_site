from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    

    class Meta:
        model = Post
        fields = ('title','body')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title here'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the content here',
                'style': 'height: 150px;'
            })
        }