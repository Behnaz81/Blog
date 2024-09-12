from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import CategoryViewSet, PostFilteredByCategory, CreatePostView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/new-post/', CreatePostView.as_view(), name="new-post"),
    path('posts-with-category/<int:cat_id>/', PostFilteredByCategory.as_view(), name="posts-filteredby-category"),
]

