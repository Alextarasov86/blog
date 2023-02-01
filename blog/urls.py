from django.conf.urls.static import static
from django.urls import path, include

from .views import *
from rest_framework import routers

app_name = 'blog'

router = routers.SimpleRouter()
router.register(r'articles', ArticlesViewSet, basename='articles')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]

