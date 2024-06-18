from django.db import models
from django.utils import timezone

# importer la  table User
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ #pour la traduction

# Creation de la table Post

class Post(models.Model):
    """
    Modèle représentant un article de blog.

    Attributes:
    """

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
