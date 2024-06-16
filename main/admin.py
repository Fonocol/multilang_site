from django.contrib import admin
from .models import Post
# Register your models here.

#admin.site.register(Post)

@admin.register(Post) #utilisation de la classe
class PostAdmin(admin.ModelAdmin):
    list_display =("title", "status","created","publish","author")
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('title', 'body')
    ordering = ("author","status","publish")
    list_filter = ('author','created','publish')