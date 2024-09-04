from django.urls import path
from my_site.views import index_view

urlpatterns = [
    path('', index_view, name="index"),
]
