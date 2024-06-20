from asyncio import streams
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _  #pour la traduction
from .models import Post
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

import ollama  # pour le llm ollama 

from django.http import HttpResponse

client = OpenAI(api_key=config('OPENAI_API_KEY'))


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
        results = Post.objects.filter(title__icontains=query) | Post.objects.filter(body__icontains=query)
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
    posts_list = Post.objects.all()
    
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

def getPost(request,slug: str):
    post = get_object_or_404(Post,slug= slug)
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
    premiermessage= _("""👋 Bonjour! Je suis AlternanceAI. N'hésitez pas à me poser des questions ou à explorer nos services. Si vous avez besoin d'aide, je suis là pour vous! 🤖✨""")
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


def ollameResponse(usermessage):
    stream = ollama.chat(model = 'mistral',messages=[{
        'role': 'user',
        'content': usermessage,
        }],
        stream = True
    )
    for chunk in stream:
        res = chunk['message']['content']
    return res

#----------------------------------------------------------------------------------------------------------------------------------------------------
#                    Chatbot developper localement: model loading
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


        # reponse du chatbot locale

        return JsonResponse({'response': bot_response})
    
    # Gérer les requêtes GET ou autres méthodes non-POST
    elif request.method == 'GET':
        return getChatbot(request)
    else:
        return HttpResponse(status=405)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------


