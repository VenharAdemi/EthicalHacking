from django.shortcuts import render
from django.db import connection
from .models import Post

def index(request):
    posts = Post.objects.all()
    return render(request, "/index.html", {"posts": posts})

def search(request):
    query = request.GET.get("q", "")
    # Vulnerable to SQL Injection
    raw_query = f"SELECT * FROM blog_post WHERE title LIKE '%{query}%'"
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        results = cursor.fetchall()
    return render(request, "/search.html", {"results": results, "query": query})


