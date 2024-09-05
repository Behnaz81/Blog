import requests
from django.shortcuts import render
from django.views import View


def index_view(request):
    posts_get = requests.get('http://localhost:8000/api/posts/')
    posts = posts_get.json()
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)

def filtered_posts(request, cat_id):
    posts_get = requests.get(f'http://localhost:8000/api/posts-with-category/{cat_id}/')
    posts = posts_get.json()
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)
