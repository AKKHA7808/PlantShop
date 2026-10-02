from decimal import Decimal

from products.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """
    ตะกร้าสินค้าแบบเก็บข้อมูลใน Django Session
    โครงสร้างข้อมูลใน session: {'cart': {'<product_id>': <quantity>, ...}}
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        """
        เพิ่มสินค้าลงตะกร้า ถ้ามีอยู่แล้วจะบวกจำนวนเพิ่ม
        คืนค่า (success: bool, message: str)
        """
        product_id = str(product.id)

        if product.stock == 0:
            return False, 'สินค้าหมด ไม่สามารถเพิ่มลงตะกร้าได้'

        current_qty = self.cart.get(product_id, 0)
        new_qty = current_qty + quantity

        if quantity <= 0:
            return False, 'จำนวนสินค้าต้องมากกว่า 0'

        if new_qty > product.stock:
            return False, f'มีสินค้าคงเหลือเพียง {product.stock} ชิ้น'

        self.cart[product_id] = new_qty
        self.save()
        return True, 'เพิ่มสินค้าลงตะกร้าเรียบร้อยแล้ว'

    def update(self, product_id, quantity):
        """ตั้งค่าจำนวนสินค้าในตะกร้าโดยตรง (ใช้ตอนกดเพิ่ม/ลดจำนวนในหน้าตะกร้า)"""
        product_id = str(product_id)
        if product_id not in self.cart:
            return False, 'ไม่พบสินค้านี้ในตะกร้า'

        product = Product.objects.filter(id=product_id).first()
        if not product:
            self.remove(product_id)
            return False, 'ไม่พบสินค้านี้ในระบบ'

        if quantity <= 0:
            return False, 'จำนวนสินค้าต้องมากกว่า 0'

        if quantity > product.stock:
            return False, f'มีสินค้าคงเหลือเพียง {product.stock} ชิ้น'

        self.cart[product_id] = quantity
        self.save()
        return True, 'อัปเดตจำนวนสินค้าเรียบร้อยแล้ว'

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.cart = {}
        self.session[CART_SESSION_KEY] = self.cart
        self.save()

    def __iter__(self):
        """คืนค่ารายการสินค้าในตะกร้าพร้อมข้อมูลสินค้าและราคารวมย่อย"""
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}

        missing_ids = set(product_ids) - set(products_map.keys())

        if missing_ids:
            for product_id in missing_ids:
                self.cart.pop(product_id, None)
            self.save()

        for product_id, quantity in self.cart.items():
            product = products_map.get(product_id)
            subtotal = product.price * quantity
            yield {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self)

    def get_total_price(self):
        total = Decimal('0')
        for item in self:
            total += item['subtotal']
        return total
