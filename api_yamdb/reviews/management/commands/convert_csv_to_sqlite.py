from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Загрузить данные из CSV файлов в базу данных'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных из CSV файлов начата')
        )

        for row in DictReader(
            open('./static/data/category.csv', encoding='utf-8', mode='r')
        ):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        for row in DictReader(
            open('./static/data/titles.csv', encoding='utf-8', mode='r')
        ):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category'])
            )
            title.save()

        for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8', mode='r')
        ):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        for row in DictReader(
            open('./static/data/users.csv', encoding='utf-8', mode='r')
        ):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()

        for row in DictReader(
            open('./static/data/genre_title.csv', encoding='utf-8', mode='r')
        ):
            genre_title = GenreTitle(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                genre=Genre.objects.get(pk=row['genre_id'])
            )
            genre_title.save()

        for row in DictReader(
            open('./static/data/review.csv', encoding='utf-8', mode='r')
        ):
            review = Review(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()

        for row in DictReader(
            open('./static/data/comments.csv', encoding='utf-8', mode='r')
        ):
            comment = Comment(
                id=row['id'],
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                pub_date=row['pub_date']
            )
            comment.save()

        self.stdout.write(
            self.style.SUCCESS('Загрузка данных из CSV файлов завершена')
        )
