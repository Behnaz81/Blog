from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import CategoryViewSet, PostFilteredByCategory, CreatePostView, ListPostsView, RetrievePostView, PostFilteredByUser, DeletePostView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/new-post/', CreatePostView.as_view(), name="new-post"),
    path('posts-with-category/<int:cat_id>/', PostFilteredByCategory.as_view(), name="posts-filteredby-category"),
    path('posts/list-posts/', ListPostsView.as_view(), name="list-posts"),
    path('posts/<int:pk>/', RetrievePostView.as_view(), name="retrieve-post"),
    path('posts/posts-with-user/', PostFilteredByUser.as_view(), name="posts-filteredby-user"),
    path('posts/delete/<int:pk>/', DeletePostView.as_view(), name="delete-post"),
]

