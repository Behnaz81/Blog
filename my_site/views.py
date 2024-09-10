import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from comments.serializers import CommentCreateSerializer


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
    if request.method == 'POST':
        print(request.POST)
        create_comment_response = requests.post(f'http://localhost:8000/api/comments/comment-add/{post_id}/', data=request.POST)
        if create_comment_response.status_code == 201:
            return HttpResponseRedirect(f'http://localhost:8000/post/{post_id}/')
        else:
            print(create_comment_response.content)
        
    # Fetch related comments
    related_comments = requests.get(f'http://localhost:8000/api/comments/comments-filtered-by-post/{post_id}/')
    related_comments_json = related_comments.json()
        
    # Comment form
    serializer = CommentCreateSerializer()


    context = {
        'post': post,
        'categories': categories,
        'related_posts': related_posts_json,
        'related_comments': related_comments_json[0:10],
        'related_comments_count': len(related_comments_json),
        'serializer': serializer,
    }

    return render(request, 'post_details.html', context)