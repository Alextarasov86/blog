from django.contrib.auth.models import User
from django.conf import settings
from .models import ViewArticle, IpAddress, Article, Category
from .serializers import ArticleSerializer

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def add_view(article, user, ip):
    addr, _ = IpAddress.objects.get_or_create(ip=ip)

    u = user if user.is_authenticated else None

    ViewArticle.objects.get_or_create(
        article=article,
        user=u,
        ip=addr
    )


ARTICLE_DATA = {
    'title': 'заголовок',
    'text': 'текст',
    'category': Category.objects.create(title='1111'),
    'images': [
        {'alt': '', 'images': 'media/images/Flag_icon.png'},
        {'alt': '', 'images': 'media/images/Gears_icon.png'},
        {'alt': '', 'images': 'media/images/Rocket_icon.png'}
]
}


def is_allowed_picture_count(images):
    return 0 < len(images) <= settings.ALLOWED_IMAGES_COUNT

def create_article(data):
    user = User.objects.get(username='alex_t')
    data['author'] = user
    upload_images = data.pop('images')
    if is_allowed_picture_count(upload_images):
        Article.objects.create(**data)


create_article(ARTICLE_DATA)

def validate_data(data):
    serializer = ArticleSerializer(data=data)
    serializer.is_valid(raise_exception=True)
