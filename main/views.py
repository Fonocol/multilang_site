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



# Create your views here.

def search(request):
    query = request.GET.get('value')

    results = []
    if query:
        results = Post.objects.filter(title__icontains=query) | Post.objects.filter(body__icontains=query)

    return results


def getPosts(request):
    hometitle = _("Explorations et Innovations du Monde Numérique")
    posts_list = Post.objects.all()
    
    paginator = Paginator(posts_list,6)
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
    
    searchResults = search(request)

    context = {
        'posts':posts,
        'page':page,
        'hometitle':hometitle,
        'searchResults':searchResults,
    }

    return render(request,'blog/post/blogs.html',context)



def getPost(request,slug: str):
    post = get_object_or_404(Post,slug= slug)
    return render(request,'blog/post/postPage.html',{'post':post})

def getAbaoutpage(request):
    return render(request,'blog/layout/abaout.html')

def getChatbot(request):
    premiermessage= """👋 Bonjour! Je suis AlternanceAI. N'hésitez pas à me poser des questions ou à explorer nos services. Si vous avez besoin d'aide, je suis là pour vous! 🤖✨"""
    return render(request,'blog/chatbotpage/chatbotpage.html',{'premiermessage':premiermessage})

@csrf_exempt  # Désactiver CSRF pour les requêtes POST venant de JavaScript
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        # Réponse automatique du bot
        bot_response = "Salut, je suis indisponible pour reponder a : "

        return JsonResponse({"response": bot_response})
    


