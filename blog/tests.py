from datetime import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError
from django.test import TestCase
from django.utils import timezone
from blog.models import Post


class PostViewTest(TestCase):
    def test_list_has_table(self):
        """Wskazany adres powinien posiadać podany parametr"""
        response = self.client.get("/post/new/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "title")

    def test_list_has_table_2(self):
        """Wskazany adres powinien posiadać podany parametr"""
        response = self.client.get("/post/new/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text")

    def test_list_has_table_3(self):
        """Wskazany adres powinien posiadać podany parametr"""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text")

    def test_list_has_table_4(self):
        """Wskazany adres powinien posiadać podany parametr"""
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "title")


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
            # Post.objects.create(title=title_name)

    def test_should_raise_max_length_exception(self):
        """Powinien zwrócić wyjątek przy zbyt długim tytule"""
        post_title = "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł" \
                     "PrzykładowyTytułPrzykładowyTytułPrzykładowyTytuł"

        with self.assertRaises(DatabaseError):
            Post.objects.create(title=post_title, author=self.user)

    def test_should_create_user(self):
        """Powinien utworzyć nowego użytkownika"""
        user_name = 'Testowy'
        user_email = '123@o2.pl'
        user_password = '12345'
        user = User.objects.create_user(username='Testowy', email='123@o2.pl', password='12345')
        user.refresh_from_db()
        self.assertEqual(user_name, user.username)
        # self.assertEqual(user_email, user.email)
        # self.assertEqual(user_password, user.password)
        user.delete()
