import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.cache import cache
from django.contrib import messages
from posts.models import Post


BASE_API_URL = 'http://localhost:8000/api/'

# Logout
def logout_user(request):
    token = request.session.get('auth_token')

    if token:
        headers = {
            'Authorization': f'Token {token}'
        }

        logout_response = requests.post(f'{BASE_API_URL}users/logout/', headers=headers)

        if logout_response.status_code == 200:
            del request.session['auth_token']
            del request.session['username']
            return redirect('my_site:index')
        
    else:
        messages.error(request, 'ابتدا وارد شوید.')
        return redirect('my_site:login')


def fetch_category(request):
    categories = cache.get('categories')

    if not categories:
        try:
            categories_response = requests.get(f'{BASE_API_URL}categories/')
            if categories_response.status_code == 200:
                categories_json = categories_response.json()
                cache.set('categories', categories_json, timeout=60*60)  
                categories = categories_json
                print('API called for categories.')
            else:
                categories = [] 

        except requests.RequestException:
            categories = []

    return categories


# Index Page
def index_view(request):
    
    if request.method == 'POST':
        return logout_user(request)

    try:
        # Fetch all posts
        posts_get = requests.get(f'{BASE_API_URL}posts/list-posts/')

        if posts_get.status_code == 200:
            posts = posts_get.json()

        else:
            posts = []

    except requests.RequestException:
        posts = []

    # Fetch categories
    categories = fetch_category(request)

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)

# Filter based on categories
def filtered_posts(request, cat_id):
    try:
        posts_get = requests.get(f'{BASE_API_URL}posts-with-category/{cat_id}/')

        if posts_get.status_code == 200:
            posts = posts_get.json()

            if not posts:
                raise Http404("No posts found for this category")
        else:
            raise Http404("Category not found")  

    except requests.RequestException:
        raise Http404("Error fetching posts for this category")

    # Fetch categories
    categories = fetch_category(request)

    context = {
        'posts': posts,
        'categories': categories
    }

    return render(request, 'index.html', context)



# Detail page
def detail_post(request, post_id):

    # Fetch post details
    post_get = requests.get(f'{BASE_API_URL}posts/{post_id}/')
    if post_get.status_code == 200:
        post = post_get.json()
    else:
        raise Http404("Post not found!")

    # Fetch categories
    categories = fetch_category(request)

    # Fetch related posts
    cat_id = post['category']['id']
    related_posts_json = []
    related_posts = requests.get(f'{BASE_API_URL}posts-with-category/{cat_id}/')
    if related_posts.status_code == 200:
        related_posts_json = related_posts.json()
        related_posts_json = [i for i in related_posts_json if not (i['id'] == post['id'])][0:5]
    
    # Submit a comment
    if request.method == 'POST':
        token = request.session.get('auth_token')

        if token:
            headers = {
                'Authorization': f'Token {token}'
            }
            
            create_comment_response = requests.post(f'{BASE_API_URL}comments/comment-add/{post_id}/', data=request.POST, headers=headers)
            if create_comment_response.status_code == 201:
                messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود.')
                return HttpResponseRedirect(f'/post/{post_id}/')
            
            else:
                messages.error(request, 'خطا در ارسال نظر، لطفا دوباره تلاش کنید.')
                return HttpResponseRedirect(f'/post/{post_id}/')
        else:
            messages.error(request, 'برای ارسال نظر ابتدا وارد شوید.')
            return HttpResponseRedirect(f'/post/{post_id}/')

      
    # Fetch related comments
    related_comments_json = []
    related_comments = requests.get(f'{BASE_API_URL}comments/comments-filtered-by-post/{post_id}/')
    if related_comments.status_code == 200:
        related_comments_json = related_comments.json()


    context = {
        'post': post,
        'categories': categories,
        'related_posts': related_posts_json,
        'related_comments': related_comments_json[0:10],
        'related_comments_count': len(related_comments_json)
    }

    return render(request, 'post_details.html', context)



# Register User
def register_user(request):

    if request.method == 'POST':
        register_user_response = requests.post(f'{BASE_API_URL}users/register/', data=request.POST)
        if register_user_response.status_code == 201:
            user = register_user_response.json().get('user')
            token = register_user_response.json().get('token') 
            
            request.session['auth_token'] = token
            request.session['username'] = user['username']
 
            return redirect('my_site:index')
        
        else:
            errors = register_user_response.json()
            custom_errors = {}
            context = {}
            
            if 'username' in errors:
                custom_errors['username'] = 'نام کاربری باید منحصر به فرد باشد و حاوی اطلاعات معتبر باشد.'
            else:
                context['username'] = request.POST['username']
            if 'password' in errors:
                if 'Ensure this field has at least 8 characters.' in errors['password']:
                    custom_errors['password'] = 'رمز عبور باید حداقل ۸ کاراکتر باشد.'
                elif 'This field may not be blank.' in errors['password']:
                    custom_errors['password'] = 'لطفا رمز عبور مناسب وارد کنید'
                else:
                    custom_errors['password'] = 'رمز عبور وارد شده صحیح نمی‌باشد.'
            if 'non_field_errors' in errors:
                if 'Passwords do not match' in errors['non_field_errors']:
                    custom_errors['password_repeat'] = 'رمز عبور و تکرار رمز عبور یکی نیست.'

            categories = fetch_category(request)
            context['categories'] = categories
            context['errors'] = custom_errors
            return render(request, 'register.html', context)
    else:
         # Fetch categories
        categories = fetch_category(request)

        context = { 
            'categories': categories
        }
        return render(request, 'register.html', context) 


# Login
def login_user(request):

    if request.method == 'POST':
        login_user_response = requests.post(f'{BASE_API_URL}users/login/', data=request.POST)
        if login_user_response.status_code == 200:
            user = login_user_response.json().get('user')
            token = login_user_response.json().get('token') 
            
            request.session['auth_token'] = token
            request.session['username'] = user['username']

            return redirect('my_site:index')
        else:
            errors = login_user_response.json()
            custom_errors = {}

            if 'non_field_errors' in errors:
                custom_errors['non_field_errors'] = 'نام کاربری یا رمز عبور نادرست است.'
            if 'username' in errors:
                custom_errors['username'] = 'لطفا نام کاربری را وارد کنید.'
            if 'password' in errors:
                custom_errors['password'] = 'لطفا رمز عبور را وارد کنید'

            categories = fetch_category(request)
            context = {
                'categories': categories, 
                'errors': custom_errors,
                'username': request.POST['username']
            }
            return render(request, 'login.html', context)
    else:
        # Fetch categories
        categories = fetch_category(request)

        context = {
            'categories': categories
        }
        
        return render(request, 'login.html', context)


# Create new post
def new_post(request):

    # Fetch Categories
    categories = fetch_category(request)

    context = {
        'categories': categories,
        'update': False
    }
    
    token = request.session.get('auth_token')

    if request.method == 'POST':

        if token:

            headers = {
                'Authorization': f'Token {token}'
            }
            
            create_post_respone = requests.post(f'{BASE_API_URL}posts/new-post/', headers=headers, data=request.POST, files=request.FILES)

            if create_post_respone.status_code == 201:
                messages.success(request, 'پست جدید با موفقیت ایجاد شد.')
                return redirect('my_site:your-posts')
            
            else:
                errors = create_post_respone.json()
                custom_errors = {}

                if 'title' in errors:
                    if 'post with this title already exists.' in errors['title']:
                        custom_errors['title'] = 'این عنوان وجود دارد.'
                    if 'This field may not be blank.' in errors['title']:
                        custom_errors['title'] = 'فیلد موضوع اجباری است.'

                if 'category' in errors:
                    if 'Incorrect type. Expected pk value, received str.' in errors['category']:
                        custom_errors['category'] = 'لطفا یک دسته بندی انتخاب کنید.'

                if 'body' in errors:
                    if 'This field may not be blank.' in errors['body']:
                        custom_errors['body'] = 'فیلد متن اجباری است.'

                context.update({
                    'title': request.POST.get('title', ''),
                    'category': request.POST.get('category', ''),
                    'body': request.POST.get('body', ''),
                    'errors': custom_errors
                })
                
                return render(request, 'new_post.html', context)
        else:
            messages.error(request, 'ابتدا وارد شوید.')
            return redirect('my_site:login')
    
    else:

        if token:
            return render(request, 'new_post.html', context)
        
        else:
            messages.error(request, 'ابتدا وارد شوید.')
            return redirect('my_site:login')


# List Posts
def list_posts(request):

    token = request.session.get('auth_token')

    if token:

        headers = {
                'Authorization': f'Token {token}'
        }

        list_posts_response = requests.get(f'{BASE_API_URL}posts/posts-with-user/', headers=headers)

        if list_posts_response.status_code == 200:
            list_posts_json = list_posts_response.json()
            context = {
                'posts': list_posts_json
            }
            return render(request, 'list_posts.html', context)
        
        else:
            messages.error(request, 'خطا در بارگذاری پست‌ها. لطفاً دوباره تلاش کنید.')
            return redirect('my_site:index')
    
    messages.error(request, 'ابتدا وارد شوید.')
    return redirect('my_site:login')
    

# Delete your post
def delete_post(request, pk):
    token = request.session.get('auth_token')

    if token:

        headers = {
                'Authorization': f'Token {token}'
        }

        delete_post_response = requests.delete(f'{BASE_API_URL}posts/delete/{pk}/', headers=headers)

        if delete_post_response.status_code == 204:
            messages.success(request, 'پست با موفقیت حذف شد.')
            return redirect('my_site:your-posts')
        
        else:
            messages.error(request, 'خطا در حذف پست‌. لطفاً دوباره تلاش کنید.')
            return redirect('my_site:index')

    messages.error(request, 'ابتدا وارد شوید.')
    return redirect('my_site:login')
    

# Update your post
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
    
