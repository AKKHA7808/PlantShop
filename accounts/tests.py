from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


class AdminLoginFlowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username='customer1',
            password='password123',
            first_name='ลูกค้า',
        )
        self.admin = User.objects.create_superuser(
            username='admin1',
            email='admin@example.com',
            password='password123',
            first_name='แอดมิน',
        )

    def test_staff_login_redirects_to_admin(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'admin1',
            'password': 'password123',
        })
        self.assertRedirects(response, reverse('admin:index'), fetch_redirect_response=False)

    def test_customer_login_redirects_to_home(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'customer1',
            'password': 'password123',
        })
        self.assertRedirects(response, reverse('products:home'))

    @override_settings(DEBUG=True)
    def test_demo_admin_login_works_in_debug(self):
        response = self.client.post(reverse('accounts:demo_admin_login'))
        self.assertRedirects(response, reverse('admin:index'), fetch_redirect_response=False)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.admin.id)

    @override_settings(DEBUG=False)
    def test_demo_admin_login_disabled_when_not_debug(self):
        response = self.client.post(reverse('accounts:demo_admin_login'))
        self.assertEqual(response.status_code, 404)
