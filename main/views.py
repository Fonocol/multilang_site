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


from difflib import get_close_matches
import random

from django.db.models import Q

# Create your views here.

#----------------------------------------------------------------------------------------------------------------------------------------------------
from django.utils.translation import get_language, activate

def change_language(request, lang_code):
    # Obtenir l'URL actuelle
    current_url = request.META.get('HTTP_REFERER', '/')
    
    # Obtenir la langue actuelle de l'URL
    current_lang = get_language()
    
    # Remplacer la langue actuelle par la nouvelle langue dans l'URL
    if current_lang in current_url:
        new_url = current_url.replace(f'/{current_lang}/', f'/{lang_code}/', 1)
    else:
        new_url = f'/{lang_code}{current_url}'

    # Activer la nouvelle langue pour l'utilisateur
    activate(lang_code)
    
    # Rediriger vers la nouvelle URL
    return redirect(new_url)



def search(request):
    """
    Fonction de recherche de post se basant sur les titres et le corps. La query est la valeur 'value' du formulaire de recherche.
    """
    query = request.GET.get('value')

    results = []

    if query:
        # Filtrage par pertinence et pondération
        results = Post.published.filter(
            Q(title__icontains=query) | 
            Q(sommary__icontains=query) | 
            Q(body__icontains=query)
        )

        # Ajouter un champ de pertinence à chaque post
        for post in results:
            relevance_score = 0
            if query.lower() in post.title.lower():
                relevance_score += 3  # Priorité plus élevée pour les titres
            if query.lower() in post.sommary.lower():
                relevance_score += 2  # Moyenne priorité pour le résumé
            if query.lower() in post.body.lower():
                relevance_score += 1  # Priorité plus faible pour le corps

            post.relevance = relevance_score  # Ajout de la pertinence au post

        # Trier par pertinence
        results = sorted(results, key=lambda post: post.relevance, reverse=True)

        # Compléter avec des résultats approximatifs si aucun résultat exact n'est trouvé
        if not results:
            results = Post.published.filter(
                Q(title__icontains=query[:3]) | 
                Q(sommary__icontains=query[:3]) | 
                Q(body__icontains=query[:3])
            )

    return results



def searchAll(request):
    """
    retourne search.html qui est la page montrant le resultat complet de la recherche
    """
    searchResults = search(request)
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
    
    searchResults = search(request)
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
    premiermessage= _("""👋 Hello! I am AlternanceAI. Feel free to ask me any questions or explore our services. If you need help, I'm here for you! 🤖✨""")
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

def load_data(file_path: str):
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_data_base(file_path: str, newdata:dict):
    with open(file_path,'w') as file:
        json.dump(newdata,file, indent=2)

def find_best_match(user_question:str, questions: list[str]):
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else  None

def get_answer(question:str,data:dict):
    for q in data['questions']:
        if q['question'] == question:
            return q['answer'][random.randint(0,len(q['answer'])-1)]



def chatbotlocal(user_input):
    #langage du bot
    current_lang = get_language()

    data: dict = load_data(current_lang+'.json')
    best_match = find_best_match(user_input, [q['question'] for q in data["questions"]])
    if best_match:
        answer: str = get_answer(best_match,data)
    else:
        answer: str = _("I'm not sure I understand. 🚀 Could you give me more details or try another question?")
    return answer
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
        bot_response = chatbotlocal(user_message)
        #bot_response = "GPT est indisponible pour repondre actullement 🤖"  #reponse alternative 

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
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)  # Ne sauvegarde pas encore dans la base de données
            
            # Assigner les valeurs manquantes
            obj.author = request.user  # Utilisateur actuellement connecté
            obj.slug = slugify(obj.title)  # Générer le slug à partir du titre
            obj.publish = timezone.now()  # Date de publication actuelle
            obj.status = 'draft'  # Statut par défaut (ou 'published' selon le besoin)

            obj.save()  # Maintenant, sauvegarde dans la base de données
            print(obj.__dict__)
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