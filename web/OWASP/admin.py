from django.contrib import admin

# Register your models here.
# blog/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
