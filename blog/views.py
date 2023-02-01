from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from .models import IpAddress, Article, Category, Comment
from .serializers import ArticleSerializer, ArticleWithCommentsSerializer, ArticleUpdateSerializer, \
    CommentUpdateSerializer, CommentDetailSerializer, CommentSerializer, CategorySerializer, \
    CategoryWithArticlesSerializer
from .services import get_client_ip, add_view


class ArticlesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend ,SearchFilter, OrderingFilter)
    filterset_fields = ('category', 'comment')
    search_fields = ('title', 'text')
    ordering_fields = ('id', 'date_created', 'title',)

    def get_queryset(self):
        qs = Article.objects.all()
        has_comments = self.request.query_params.get('has_comments', None)
        has_views = self.request.query_params.get('has_views', None)

        if has_views == 'true':
            qs = qs.filter(views__gte=1)
        if has_views == 'false':
            qs = qs.filter(views=None)

        if has_comments is not None:
            qs = qs.annotate(comment__count=Count('comment'))

        if has_comments == 'true':
            qs = qs.filter(comment__count__gte=1)
        if has_comments == 'false':
            qs = qs.filter(comment__count=0)
        if self.request.user.is_superuser:
            return qs

        return qs.filter(is_published=True)

    def get_serializer(self, instance=None, **kwargs):
        if self.action == 'retrieve':
            return ArticleWithCommentsSerializer(instance, **kwargs)
        if self.action in ['update', 'partial_update']:
            return ArticleUpdateSerializer(instance, **kwargs)
        return ArticleSerializer(instance, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        ip = get_client_ip(request)

        add_view(obj, request.user, ip)

        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        data = {
            'title': request.data['title'],
            'text': request.data['text'],
            'category': request.data['category'],
            'author': request.user.id
        }

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({ 'errors': serializer.errors})
        cat = Category.objects.get(id=data['category'])
        if cat.admin_category:
            return Response({'errors': {'category': 'добавлять в эту категорию может только админ'}})
        self.perform_create(serializer)
        return Response({ 'detail': 'Ваша статья отправлена на модерацию'})

    def update(self, request, *args, pk=None):
        try:
            article = self.get_queryset().get(pk=pk)
        except:
            Response ({}, status=404)

        if not request.user.is_superuser:
            if article.author != request.user:
                return Response({'Вы не можете редактировать эту статью'}, status=403)

        data = {
            'title': request.data['title'],
            'text': request.data['text'],
            'category': request.data['category'],
            'is_published': False
            }

        if request.user.is_superuser:
            data['is_published'] = True

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors})

        self.perform_update(serializer)

        return Response({ 'detail': 'Изменения успешно добавлены' if request.user.is_superuser else 'Ваша статья отправлена на модерацию'})

    # def retrieve(self, request, pk=None):
    #     try:
    #         article = self.get_queryset().get(pk=pk)
    #     except:
    #         return Response({}, status=404)
    #     return Response ({
    #         'result': ArticleWithCommentsSerializer(article).data
    #     })


class CommentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Comment.objects.filter(parent=None)
        return Comment.objects.filter(is_published=True).filter(parent=None)

    def get_serializer(self, instance=None, **kwargs):
        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer(instance, **kwargs)
        return CommentDetailSerializer(instance, **kwargs)

    def create(self, request, *args, **kwargs):
        data = {
            'text': request.data['text'],
            'article': request.data['article'],
            'parent': request.data['parent'],
            'author': request.user.id,
        }
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({ 'errors': serializer.errors})
        self.perform_create(serializer)
        return Response({ 'detail': 'Комментарий успешно добавлен' if request.user.is_superuser else 'Ваш комментарий отправлен на модерацию'})

    def update(self, request, *args, pk=None):
        try:
            comment = self.get_queryset().get(pk=pk)
        except:
            Response({'Комментарий не найден'}, status=404)

        if not request.user.is_superuser:
            if comment.author != request.user:
                return Response({'Вы не можете редактировать этот комментарий'}, status=403)

        data = {
            'text': request.data['text'],
            'is_published': False
        }

        if request.user.is_superuser:
            data['is_published'] = True

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors})
        self.perform_update(serializer)

        return Response({'detail': 'Изменения успешно добавлены' if request.user.is_superuser else 'Ваш комментарий отправлен на модерацию'})


    def destroy(self, request, pk=None):
        try:
            comment = self.get_queryset().get(pk=pk)
        except:
            Response ({}, status=404)

        if not request.user.is_superuser:
            if comment.author != request.user:
                return Response({}, status=403)

        comment.delete()
        return Response({'Комментарий успешно удален'})

    @action(detail=False, methods=['get'], url_path='my')
    def get_comment_user(self, request):
        comments = Comment.objects.filter(author=request.user)
        return Response({
            'result': CommentSerializer(comments, many=True).data
        })


class CategoriesViewSet(viewsets.ModelViewSet):
    # permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('title', )

    def get_serializer(self, instance=None, **kwargs):
        if self.action == 'retrieve':
            return CategoryWithArticlesSerializer(instance, **kwargs)
        return CategorySerializer(instance, **kwargs)
