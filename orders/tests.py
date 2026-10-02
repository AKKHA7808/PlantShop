from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class OrderAndCartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.product = Product.objects.create(name='Test Plant', price=100.0, stock=5)

    def test_empty_cart_cannot_checkout(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('orders:checkout'))
        self.assertRedirects(response, reverse('products:product_list'))

    def test_order_detail_requires_login(self):
        response = self.client.get(reverse('orders:order_detail', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_customer_cannot_view_another_customers_order(self):
        from orders.models import Order
        order = Order.objects.create(user=self.user1, receiver_name='U1', phone='123', total_price=100.0)
        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('orders:order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 404)

    def test_successful_checkout_reduces_stock_and_creates_order(self):
        self.client.login(username='user1', password='password')
        # Add to cart
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 2})
        # Checkout
        response = self.client.post(reverse('orders:checkout'), {
            'receiver_name': 'Test User',
            'phone': '0812345678',
            'shipping_address': 'Test Address'
        })
        self.assertEqual(response.status_code, 302)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3) # 5 - 2 = 3
        
        from orders.models import Order, OrderDetail
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)

    def test_cart_prevents_quantity_greater_than_stock(self):
        self.client.login(username='user1', password='password')
        # Add to cart with quantity > stock (5)
        response = self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 10})
        self.assertRedirects(response, reverse('cart:cart_detail'))
        # The quantity in cart should not exceed stock, cart logic caps it.
        # Let's try checkout with valid cart but then change stock
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 3})
        self.product.stock = 1
        self.product.save()
        response = self.client.post(reverse('orders:checkout'), {
            'receiver_name': 'Test User',
            'phone': '0812345678',
            'shipping_address': 'Test Address'
        })
        self.assertRedirects(response, reverse('cart:cart_detail'))
        
    def test_product_deleted_after_added_to_cart(self):
        self.client.login(username='user1', password='password')
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 1})
        self.product.delete()
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        # Should not crash
