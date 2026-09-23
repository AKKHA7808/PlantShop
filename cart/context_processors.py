from .cart import Cart


def cart_summary(request):
    """เพิ่มตัวแปร cart_count ให้ใช้ได้ในทุก template (สำหรับแสดงใน Navbar)"""
    cart = Cart(request)
    return {'cart_count': len(cart)}
