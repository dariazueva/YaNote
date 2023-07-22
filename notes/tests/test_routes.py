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
            # ('notes:add', None)
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_show_and_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_note_add(self):
        self.client.force_login(self.author)
        url = reverse('notes:add', None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_a_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in ('notes:edit', 'notes:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_b_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        url = reverse('notes:add', None)
        redirect_url = f'{login_url}?next={url}'
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)