import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_genre(self, value):
        for slug in value:
            if not get_object_or_404(Genre, slug=slug):
                raise serializers.ValidationError(
                    "Указанный жанр не существует"
                )
        return value

    def validate_category(self, value):
        if not (
            self.request.data.get('category')
            and get_object_or_404(Category, slug=value)
        ):
            raise serializers.ValidationError(
                "Указанная категория не существует"
            )
        return value

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value

    def get_rating(self, obj):
        return obj.avg_rating


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        request = self.context.get('request')
        title_id = request.parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = request.user
        if (
            request.method == 'POST'
            and user.reviews.filter(title=title).exists()
        ):
            raise serializers.ValidationError("Нельзя оставить второй отзыв")
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError(
                'Оценка за пределами допустимого диапазона'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
