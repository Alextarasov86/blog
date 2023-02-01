from django.db import models
from django.contrib.auth.models import User
from users.models import IpAddress


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    admin_category = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}. {self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)
    preview = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticlePicture(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    alt = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.id}. [{self.article}] {self.alt}'


class ViewArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author.username} на {self.article}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True