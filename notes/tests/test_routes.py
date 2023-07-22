from http import HTTPStatus

from django.contrib.auth import get_user_model

from django.test import TestCase

from django.urls import reverse

from notes.models import Note


User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Брэд Пит')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author)
        cls.reader = User.objects.create(username='Анон')

    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            # ('notes:list', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page(self):
        self.client.force_login(self.author)
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


