from django.urls import path
from my_site.views import index_view, filtered_posts

app_name = "my_site"

urlpatterns = [
    path('', index_view, name="index"),
    path('<int:cat_id>/', filtered_posts, name="filtered"),
]
