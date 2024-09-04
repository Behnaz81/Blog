from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CategoryViewSet, index_view

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index_view, name="index"),
]

