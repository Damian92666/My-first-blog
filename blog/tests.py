from datetime import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from blog.models import Post


class PostTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("username")

    def test_should_create_title(self):
        """Powinien utworzyć poprawny tytuł"""
        post_title = "Python"
        post = Post.objects.create(title=post_title, author=self.user)
        post.refresh_from_db()

        self.assertEqual(post_title, post.title)
        post.delete()

    def test_should_create_text(self):
        """Powinien utworzyć poprawny tekst"""
        post_text = "Język programowania wysokiego poziomu ogólnego przeznaczenia," \
                    " o rozbudowanym pakiecie bibliotek standardowych, " \
                    "którego ideą przewodnią jest czytelność i klarowność kodu źródłowego. " \
                    "Jego składnia cechuje się przejrzystością i zwięzłością."
        text = Post.objects.create(text=post_text, author=self.user)
        text.refresh_from_db()

        self.assertEqual(post_text, text.text)
        text.delete()

    def test_should_create_date(self):
        """Powinien utworzyć poprawną datę napisanego posta"""
        post_date = "2020-01-02 20:20:20"
        date = Post.objects.create(created_date=post_date, author=self.user)
        date.refresh_from_db()

        self.assertEqual(timezone.localtime(timezone.make_aware(datetime.fromisoformat(post_date))),
                         timezone.localtime(date.created_date))
        date.delete()

    def test_should_create_published_date(self):
        """Powinien utworzyć poprawną datę dodania posta"""
        post_date = "2020-02-02 20:20:20"
        date = Post.objects.create(published_date=post_date, author=self.user)
        date.refresh_from_db()

        self.assertEqual(timezone.localtime(timezone.make_aware(datetime.fromisoformat(post_date))),
                         timezone.localtime(date.published_date))
        date.delete()

    def test_should_raise_null_exception(self):
        with self.assertRaises(IntegrityError):
            Post.objects.create(title=None)

    def test_should_raise_unique_exception(self):
        title_name = "Python"
        with self.assertRaises(IntegrityError):
            Post.objects.create(title=title_name)
            Post.objects.create(title=title_name)


    # def test_should_raise_max_length_exception(self):
    #     """Powinien zwrócić wyjątek przy zbyt długim tytule"""
    #     post_title = "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł" \
    #                  "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł" \
    #                  "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł" \
    #                  "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł"
    #     Post.objects.create(title=post_title, author=self.user)
