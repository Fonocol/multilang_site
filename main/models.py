from django.db import models
from django.utils import timezone

# importer la  table User
from django.contrib.auth.models import User

# Creation de la table Post

class Post(models.Model):
    STATUS_CHOICES = (
        ("draft","Draft"),
        ("published","published"),
    )
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES,default="draft",max_length=10)
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted")

    def __str__(self)-> str:
        return self.title


#Django@2002.com
#Fono2002.com
#venv\Scripts\activate.bat

#tranlation :
#python manage.py makemassages
#python manage.py compilemessages
#python manage.py compilemessages

#
#