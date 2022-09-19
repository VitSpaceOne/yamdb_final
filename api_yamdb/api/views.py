from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title
from users.permissions import Admin, Moderator, ReadOnly, Superuser, User

from .filters import TitleFilter
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitlesSerializer)
from .viewsets import GetPostPatchDeleteViewSet, ListCreateDestoryViewSet


class CategoriesViewSet(ListCreateDestoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'slug')
    permission_classes = [Superuser | Admin | ReadOnly]
    pagination_class = PageNumberPagination


class GenresViewSet(ListCreateDestoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'slug')
    permission_classes = [Superuser | Admin | ReadOnly]
    pagination_class = PageNumberPagination


class TitlesViewSet(GetPostPatchDeleteViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [Superuser | Admin | ReadOnly]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        category = Category.objects.get(slug=self.request.data.get('category'))
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        category = Category.objects.get(slug=self.request.data.get('category'))
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)


class ReviewsViewSet(GetPostPatchDeleteViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [Superuser | Admin | Moderator | User | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(GetPostPatchDeleteViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [Superuser | Admin | Moderator | User | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
