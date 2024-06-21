from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from utilisateurs.forms import RegistForms

# Create your views here.

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)  #verifier si l'utilisateur exixte
            if user is not None:
                login(request, user)
                return redirect('getPosts')
            else:
                return render(request, 'registration/login.html',{})
        else:
            return render(request, 'registration/login.html',{})
    else:
        return redirect('getPosts')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('getPosts')
    else:
        return redirect('getPosts')

def registration_view(request):
    if request.method == 'POST':
        user_form = RegistForms(request.POST)    #user informations to creat an account
        # creation de l'utilisateur
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])  #to clean password in forms
            new_user.save()
            return redirect('login_view')
        else:
            return render(request, 'registration/register.html',{"user_form":user_form})
    
    else:
        #get un formulaire
        user_form = RegistForms()
        return render(request, 'registration/register.html',{"user_form":user_form})