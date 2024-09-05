from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CategoryViewSet, PostFilteredByCategory

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts-with-category/<int:cat_id>/', PostFilteredByCategory.as_view(), name="posts-filteredby-category"),
]

