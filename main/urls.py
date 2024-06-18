from django.urls import path
from . import views

#router
urlpatterns = [
    path('', views.getPosts, name="getPosts"),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('about/', views.getAbaoutpage, name="getAbaoutpage"),
    path('search/', views.searchAll, name="searchAll"),
    path('<slug>/', views.getPost, name="getPost"),
]



