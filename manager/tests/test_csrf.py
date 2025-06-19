from django.test import TestCase, Client
from django.urls import reverse


class CSRFProtectionTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_login_csrf_protection(self):
        # Пытаемся отправить POST без CSRF токена
        response = self.client.post(
            reverse('manager:login'),
            {'username': 'test', 'password': 'test'}
        )
        # Должны получить 403 Forbidden из-за отсутствия CSRF токена
        self.assertEqual(response.status_code, 403)

    def test_login_with_csrf(self):
        # Сначала получаем страницу, чтобы получить CSRF токен
        get_response = self.client.get(reverse('manager:login'))
        csrf_token = self.client.cookies['csrftoken'].value

        # Теперь отправляем POST с CSRF токеном
        response = self.client.post(
            reverse('manager:login'),
            {
                'username': 'test',
                'password': 'test',
                'csrfmiddlewaretoken': csrf_token
            },
            follow=True
        )
        # Проверяем, что форма была отправлена (хотя аутентификация может не пройти)
        self.assertNotEqual(response.status_code, 403)