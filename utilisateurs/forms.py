from django import forms
from django.contrib.auth.models import User


class RegistForms(forms.ModelForm):

    username = forms.CharField(
        label='Username',
        max_length=250,
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "username",
            "type": "text",
            "placeholder": "Username",
            "data-sb-validations": "required"
        })
    )

    first_name = forms.CharField(
        label='First Name',
        max_length=250,
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "first_name",
            "type": "text",
            "placeholder": "First Name",
            "data-sb-validations": "required"
        })
    )

    last_name = forms.CharField(
        label='Last Name',
        max_length=250,min_length=5,
        help_text='',
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "lastName",
            "type": "text",
            "placeholder": "Last Name",
            "data-sb-validations": "required"
        })
    )

    email = forms.EmailField(
        label='Email Address',
        max_length=250,min_length=5,
        help_text='',
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "emailAddress",
            "type": "email",
            "placeholder": "Email Address",
            "data-sb-validations": "required,email"
        })
    )

    password = forms.CharField(
        label='Password',
        max_length=250,min_length=8,
        help_text='',
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "password",
            "type": "password",
            "placeholder": "Password",
            "data-sb-validations": "required"
        })
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        max_length=250,min_length=8,
        help_text='',
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "confirmPassword",
            "type": "password",
            "placeholder": "Confirm Password",
            "data-sb-validations": "required"
        })
    )


    class Meta:
        model = User
        fields = ('username','first_name','last_name','email') #recuperation des  champs du formulaire de django