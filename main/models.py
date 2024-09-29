from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# importer la  table User
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ #pour la traduction

# Creation de la table Post

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

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
    sommary = models.CharField(max_length=250, verbose_name=_("Sommary"))
    body = models.TextField(verbose_name=_("Body"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default="draft", max_length=10, verbose_name=_("Status"))
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted")
    
    objects = models.Manager # manager par defaut
    published = PublishedManager() 


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self)-> str:
        return self.title
    
    #urls personnalisable
    def get_absolute_url(self):
        return reverse("getPost", args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

    #creation des slugs a la creation du post  
    # surchage la methode save  
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
        print('je suis sur que il ya un probleme')



#Django@2002.com ++++ Fono++++ eilco@cm
#Fono2002.com
#venv\Scripts\activate.bat

#tranlation :
#python manage.py makemassages
#python manage.py compilemessages
#python manage.py compilemessages
