from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.getPosts, name="getPosts"),
    path('chatbat/', views.getChatbot, name="getChatbot"),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('about/', views.getAbaoutpage, name="getAbaoutpage"),
    path('search/', views.searchAll, name="searchAll"),
    path('<slug>/', views.getPost, name="getPost"),
]



urlpatterns += staticfiles_urlpatterns()