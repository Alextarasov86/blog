from django.db.models import Q
from rest_framework import serializers
from .models import Article, Comment, Category, ViewArticle
from users.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    views = serializers.SerializerMethodField()

    def get_views(self, obj):
        count = ViewArticle.objects.filter(article=obj).count()
        return count

    class Meta:
        model = Article
        fields = '__all__'


class ArticleUpdateSerializer(serializers.ModelSerializer):
    date_created = serializers.CharField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return [x.id for x in obj.children()]
        return []

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'date_created', 'reply_count', 'replies', 'parent')


class CommentDetailSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        if obj.is_parent:
            return [x.id for x in obj.children()]
        return []

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    class Meta:
        model = Comment
        fields = ('id', 'article', 'parent', 'author', 'text', 'replies', 'date_created', 'reply_count')


class CommentUpdateSerializer(serializers.ModelSerializer):
    date_created = serializers.CharField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    def get_views(self, obj):
        count = ViewArticle.objects.filter(article=obj).count()
        return count

    def get_comments(self, article):
        comments = Comment.objects.filter(article=article)
        return CommentSerializer(comments, many=True).data

    def get_author(self, article):
        return UserSerializer(article.author).data

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'date_created', 'comments', 'is_published', 'views')

class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    def get_articles(self, category):
        articles = Article.objects.filter(category=category)
        return ArticleSerializer(articles, many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'articles')


class CategoryWithArticlesSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    def get_articles(self, category):
        articles = Article.objects.filter(
            Q(category=category) | Q(category__parent=category)
        )
        return ArticleSerializer(articles, many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'parent', 'articles')



# class ArticleWithCategorySerializer(serializers.ModelSerializer):
#     category = serializers.SerializerMethodField()
#
#     def get_category(self, article):
#         category = Category.objects.filter(id=article.category)
#         return CategorySerializer(category).data
#
#     class Meta:
#         model = Article
#         fields = ('id', 'title', 'text', 'category')