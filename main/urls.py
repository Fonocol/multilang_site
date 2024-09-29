from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#router
urlpatterns = [
    path('', views.getHome, name="getHome"),
    path('home/', views.getPosts, name="getPosts"),
    path('chatbot/', views.chatbot_view, name='chatbot_view'),
    path('about/', views.getAbaoutpage, name="getAbaoutpage"),
    path('search/', views.searchAll, name="searchAll"),
    path('addpost/', views.add_post, name="add_post"),
    path('profil/', views.profil, name="profil"),
    path('change_language/<str:lang_code>/', views.change_language, name='change_language'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', views.getPost, name="getPost"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



