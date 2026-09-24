from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="ต้นไม้ทดสอบ")
        self.product = Product.objects.create(
            name="ต้นไม้ A",
            description="ทดสอบ",
            price=100.00,
            stock=10,
            category=self.category
        )

    def test_product_list_loads(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ต้นไม้ A")

    def test_invalid_category_query(self):
        response = self.client.get(reverse('products:product_list') + '?category=abc')
        self.assertEqual(response.status_code, 200)

    def test_product_search(self):
        response = self.client.get(reverse('products:product_list') + '?q=ต้นไม้')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ต้นไม้ A")
