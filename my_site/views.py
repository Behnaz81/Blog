import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from comments.serializers import CommentCreateSerializer


BASE_API_URL = 'http://localhost:8000/api/'

def index_view(request):

    # Fetch all posts
    posts_get = requests.get('http://localhost:8000/api/posts/')
    posts = posts_get.json()

    # Fetch categories
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)

def filtered_posts(request, cat_id):

    # Fetch posts with a known category
    posts_get = requests.get(f'http://localhost:8000/api/posts-with-category/{cat_id}/')
    posts = posts_get.json()

    # Fetch categories
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)

def detail_post(request, post_id):

    # Fetch post details
    post_get = requests.get(f'http://localhost:8000/api/posts/{post_id}/')
    post = post_get.json()

    # Fetch categories
    categories_get = requests.get('http://localhost:8000/api/categories/')
    cat_id = post['category']['id']
    categories = categories_get.json()

    # Fetch related posts
    related_posts = requests.get(f'http://localhost:8000/api/posts-with-category/{cat_id}/')
    related_posts_json = related_posts.json()
    related_posts_json = [i for i in related_posts_json if not (i['id'] == post['id'])][0:5]
    
    # Submit a comment
    form_errors=[]
    if request.method == 'POST':
        create_comment_response = requests.post(f'http://localhost:8000/api/comments/comment-add/{post_id}/', data=request.POST)
        if create_comment_response.status_code == 201:
            return HttpResponseRedirect(f'http://localhost:8000/post/{post_id}/')
        
    # Fetch related comments
    related_comments = requests.get(f'http://localhost:8000/api/comments/comments-filtered-by-post/{post_id}/')
    related_comments_json = related_comments.json()


    context = {
        'post': post,
        'categories': categories,
        'related_posts': related_posts_json,
        'related_comments': related_comments_json[0:10],
        'related_comments_count': len(related_comments_json),
        'form_errors': form_errors
    }

    return render(request, 'post_details.html', context)


def register_user(request):

    # Fetch categories
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'categories': categories
    }

    if request.method == 'POST':
        register_user_response = requests.post(f'{BASE_API_URL}users/register/', data=request.POST)
        if register_user_response.status_code == 201:
            token = register_user_response.json().get('token') 
            print(token)
            return HttpResponseRedirect(f'http://localhost:8000/')
        else:
            print(register_user_response.content)
            return HttpResponseRedirect(f'http://localhost:8000/')
    else:
        return render(request, 'register.html', context)        
