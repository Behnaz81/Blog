from django.urls import path
from my_site.views import index_view, filtered_posts, detail_post, register_user, login_user, new_post, list_posts, delete_post, update_post, logout_user

app_name = "my_site"

urlpatterns = [
    path('', index_view, name="index"),
    path('<int:cat_id>/', filtered_posts, name="filtered"),
    path('post/<int:post_id>/', detail_post, name="detail-post"),
    path('register/', register_user, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('new-post/', new_post, name="new-post"),
    path('your-posts/', list_posts, name="your-posts"),
    path('delete/<int:pk>/', delete_post, name="delete-post"),
    path('update/<int:pk>/', update_post, name="update-post"),
]
