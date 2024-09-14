import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from posts.models import Post


BASE_API_URL = 'http://localhost:8000/api/'

# Logout
def logout_user(request):

    token = request.session.get('auth_token')
    headers = {
        'Authorization': f'Token {token}'
    }

    logout_response = requests.post(f'{BASE_API_URL}users/logout/', headers=headers)

    if logout_response.status_code == 200:
        del request.session['auth_token']
        del request.session['username']
        return redirect('my_site:index')
    
    else:
        return redirect('my_site:index')


def index_view(request):

    token = request.session.get('auth_token')

    if token:
        logged_in = True
    else:
        logged_in = False

    if request.method == 'POST':
        logout_user(request)

    # Fetch all posts
    posts_get = requests.get(f'{BASE_API_URL}posts/list-posts/')
    posts = posts_get.json()

    # Fetch categories
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'posts': posts,
        'categories': categories,
        'logged_in': logged_in
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
    post_get = requests.get(f'{BASE_API_URL}posts/{post_id}/')
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
        token = request.session.get('auth_token')

        headers = {
            'Authorization': f'Token {token}'
        }
        
        create_comment_response = requests.post(f'{BASE_API_URL}comments/comment-add/{post_id}/', data=request.POST, headers=headers)
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
            user = register_user_response.json().get('user')
            token = register_user_response.json().get('token') 
            
            request.session['auth_token'] = token
            request.session['username'] = user['username']
 
            return redirect('my_site:index')
        else:
            print(register_user_response.content)
            return HttpResponseRedirect(f'http://localhost:8000/')
    else:
        return render(request, 'register.html', context) 


def login_user(request):

    if request.method == 'POST':
        register_user_response = requests.post(f'{BASE_API_URL}users/login/', data=request.POST)
        if register_user_response.status_code == 200:
            user = register_user_response.json().get('user')
            token = register_user_response.json().get('token') 
            
            request.session['auth_token'] = token
            request.session['username'] = user['username']

            return redirect('my_site:index')
        else:
            print(register_user_response.content)
            return HttpResponseRedirect(f'http://localhost:8000/')
    else:
        # Fetch categories
        categories_get = requests.get('http://localhost:8000/api/categories/')
        categories = categories_get.json()

        context = {
            'categories': categories
        }
        
        return render(request, 'login.html', context)


def new_post(request):
    categories_get = requests.get('http://localhost:8000/api/categories/')
    categories = categories_get.json()

    context = {
        'categories': categories,
        'update': False
    }

    if request.method == 'POST':
        token = request.session.get('auth_token')

        headers = {
            'Authorization': f'Token {token}'
        }
        
        create_post_respone = requests.post(f'{BASE_API_URL}posts/new-post/', headers=headers, data=request.POST, files=request.FILES)

        if create_post_respone.status_code == 201:
            return redirect('my_site:index')
        
        else:
            print(create_post_respone.content)
            return redirect('my_site:index')
    
    else:
        return render(request, 'new_post.html', context)


def list_posts(request):

    token = request.session.get('auth_token')

    headers = {
            'Authorization': f'Token {token}'
    }

    list_posts_response = requests.get(f'{BASE_API_URL}posts/posts-with-user/', headers=headers)
    list_posts_json = list_posts_response.json()

    context = {
        'posts': list_posts_json
    }

    if list_posts_response.status_code == 200:
        return render(request, 'list_posts.html', context)
    
    return redirect('my_site:index')

def delete_post(request, pk):
    token = request.session.get('auth_token')

    headers = {
            'Authorization': f'Token {token}'
    }

    delete_post_response = requests.delete(f'{BASE_API_URL}posts/delete/{pk}/', headers=headers)

    if delete_post_response.status_code == 204:
        return redirect('my_site:your-posts')

    return redirect('my_site:index')
    
def update_post(request, pk):
    token = request.session.get('auth_token')

    headers = {
            'Authorization': f'Token {token}'
    }

    if request.method == 'POST':

        update_post_response = requests.patch(f'{BASE_API_URL}posts/update/{pk}/', headers=headers, data=request.POST, files=request.FILES)

        if update_post_response.status_code == 200:
            return redirect('my_site:your-posts')

    else:
        list_posts_response = requests.get(f'{BASE_API_URL}posts/posts-with-user/', headers=headers)
        list_posts_json = list_posts_response.json()

        # Fetch post details
        post_get = requests.get(f'{BASE_API_URL}posts/{pk}/')
        post = post_get.json()

        if post in list_posts_json:
            context = {
                'post': post,
                'update': True
            }

            return render(request, 'new_post.html', context)
        
        return redirect('my_site:your-posts')
    
    