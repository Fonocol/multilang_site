from asyncio import streams
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _  #pour la traduction
from .models import Post
from main.forms import PostForm
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
from decouple import config

from django.http import HttpResponse

client = OpenAI(api_key=config('OPENAI_API_KEY'))
from django.utils.text import slugify
from django.utils import timezone

# Create your views here.

#----------------------------------------------------------------------------------------------------------------------------------------------------
def search(request):
    """
    fonction de recherche de post ce basant sur les titre et le body query est la valeur value du formulaire de recherche
    """
    query = request.GET.get('value')

    results = []
    augmented_results = []
    if query:
        results = Post.published.filter(title__icontains=query) | Post.published.filter(body__icontains=query)
    return (results,augmented_results)


def searchAll(request):
    """
    retourne search.html qui est la page montrant le resultat complet de la recherche
    """
    searchResults = search(request)[0]
    return render(request,'blog/post/search.html',{'searchResults':searchResults})

#----------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------
def getPosts(request):
    hometitle = _("Explorations and Innovations in the Digital World")
    posts_list = Post.published.all()
    
    paginator = Paginator(posts_list,4)
    page = request.GET.get('page')
    try:
        # recuperation des donner de la page x = page 
        posts = paginator.page(page)
    except PageNotAnInteger:
        #revenir a la premiere page si la page n'est pas un entier
        posts = paginator.page(1)
    except EmptyPage:
        # si la page n'est pas existante aller a la page de fin
        posts = paginator.page(paginator.num_pages)
    
    searchResults = search(request)[0]
    query = request.GET.get('value')

    context = {
        'posts':posts,
        'page':page,
        'hometitle':hometitle,
        'searchResults':searchResults,
        'query':query,
    }

    return render(request,'blog/post/blogs.html',context)

def getPost(request,year:int, month:int ,day:int,slug: str):
    post = get_object_or_404(Post,slug= slug,status="published",publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/postPage.html',{'post':post})

#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

def getAbaoutpage(request):
    return render(request,'blog/layout/abaout.html')

#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

def getChatbot(request):
    """
    retourne la page chatbotpage.html qui est la page de chatbot
    """
    premiermessage= """👋 Bonjour! Je suis AlternanceAI. N'hésitez pas à me poser des questions ou à explorer nos services. Si vous avez besoin d'aide, je suis là pour vous! 🤖✨"""
    return render(request,'blog/chatbotpage/chatbotpage.html',{'premiermessage':premiermessage})


def getGPTResponse(query):
    """
    retourne la reponse de GPT
    """
    
    MODEL = "gpt-3.5-turbo"
    # example with a system message
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "tu est un  assistant qui aide en repondant tres simplement au question brievement."},
        {"role": "user", "content": query},
    ],
    temperature=0,
    )
    suggestions = response.choices[0].message.content

    return suggestions

#----------------------------------------------------------------------------------------------------------------------------------------------------
#  --------------- UTILISATIO DU MODEL LOCALE
#----------------------------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------



@csrf_exempt  # Désactiver CSRF pour les requêtes POST venant de JavaScript
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        # Réponse automatique du bot
        # Ajouter un API key pour GPT
        #bot_response = getGPTResponse(user_message)#"Salut, je suis indisponible pour repondre :-)"
        #bot_response = ollameResponse(user_message)
        bot_response = "GPT est indisponible pour repondre actullement 🤖"  #reponse alternative 

        return JsonResponse({'response': bot_response})
    
    # Gérer les requêtes GET ou autres méthodes non-POST
    elif request.method == 'GET':
        return getChatbot(request)
    else:
        return HttpResponse(status=405)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------




def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)  # Ne sauvegarde pas encore dans la base de données
            
            # Assigner les valeurs manquantes
            newForm.author = request.user  # Utilisateur actuellement connecté
            newForm.slug = slugify(newForm.title)  # Générer le slug à partir du titre
            newForm.publish = timezone.now()  # Date de publication actuelle
            newForm.status = 'draft'  # Statut par défaut (ou 'published' selon le besoin)

            newForm.save()  # Maintenant, sauvegarde dans la base de données
            return redirect('getPosts')  # Rediriger après la sauvegarde réussie
        else:
            # Affiche les erreurs de validation dans les logs pour le débogage
            print(form.errors)
            return render(request, 'blog/post/addpost.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'blog/post/addpost.html', {'form': form})

def profil(request):
    return render(request, 'blog/layout/profil.html', {})