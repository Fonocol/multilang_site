from django.urls import path
from . import views

#router
urlpatterns = [
    path('', views.getPosts, name="getPosts"),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('about/', views.getAbaoutpage, name="getAbaoutpage"),
    path('search/', views.searchAll, name="searchAll"),
    path('addpost/', views.add_post, name="add_post"),
    path('profil/', views.profil, name="profil"),
    path('<int:year>/<int:month>/<int:day>/<slug>/', views.getPost, name="getPost"),
]



