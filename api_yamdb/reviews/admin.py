from django.contrib import admin
from users.models import User

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'bio'
    )
    search_fields = ('email',)
    list_filter = ('email',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'description'
    )
    search_fields = ('name',)
    list_filter = ('name', 'genre')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date'
    )


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'genre'
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
