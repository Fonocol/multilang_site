from django.db import models
from django.utils import timezone

# importer la  table User
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Creation de la table Post

#lass Post(models.Model):
#   STATUS_CHOICES = (
#       ("draft","Draft"),
#       ("published","published"),
#   )
#   title = models.CharField(max_length=200)
#   slug  = models.SlugField(max_length=200)
#   body = models.TextField()
#   created = models.DateTimeField(auto_now_add=True)
#   updated = models.DateTimeField(auto_now=True)
#   status = models.CharField(choices=STATUS_CHOICES,default="draft",max_length=10)
#   publish = models.DateTimeField(default=timezone.now)
#   author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted")
#
#   def __str__(self)-> str:
#       return self.title



class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", _("Draft")),
        ("published", _("Published")),
    )
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200)
    body = models.TextField(verbose_name=_("Body"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default="draft", max_length=10, verbose_name=_("Status"))
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

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