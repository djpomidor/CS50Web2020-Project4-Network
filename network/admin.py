from django.contrib import admin
from .models import User, Post

class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created")

class UsersAdmin(admin.ModelAdmin):
    list_users = ("id", "name")

# Register your models here.
admin.site.register(User, UsersAdmin)
admin.site.register(Post, PostsAdmin)
