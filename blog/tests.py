from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .services import create_article
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from .models import Category, Article
from .views import ArticlesViewSet, CategoriesViewSet



User = get_user_model()


ARTICLE_DATA = {
    'title': 'заголовок',
    'text': 'текст',
    'category': 1,
    'preview': [
        {'alt': '', 'images': ''},
        {'alt': '', 'images': ''}
    ]
}

class ArticleCreateTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ArticlesViewSet.as_view({'get': 'list', 'post': 'create'})
        self.url = '/v1/blog/articles/'
        self.user = User.objects.create(username='test1', email='alex_test@mail.ru', password='1q2w3e4r')
        self.category = Category.objects.create(title='cat_test_1')


    def test_create_article(self):
        article_test = {'title': 'article1', 'text': 'test_text', 'category': self.category.id, 'author': self.user}

        request = self.factory.post(self.url, article_test)
        request.user = self.user
        response = self.view(request)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_article(self):
        factory = APIRequestFactory()
        request = self.factory.put('/v1/blog/articles/3/', {'title': 'Статья 303'})
        request.user = self.user
        response = self.view(request)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #
#
#

