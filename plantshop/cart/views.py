from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from products.models import Product

from .cart import Cart


def cart_detail_view(request):
    """หน้าตะกร้าสินค้า - แสดงรายการ, ราคารวม"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add_view(request, product_id):
    """เพิ่มสินค้าลงตะกร้า (เรียกจากหน้ารายการสินค้า/รายละเอียดสินค้า)"""
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart = Cart(request)
    success, message = cart.add(product, quantity)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    # กลับไปหน้าที่กดมา ถ้าไม่มีให้กลับไปตะกร้า
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart:cart_detail'
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = 'cart:cart_detail'
    return redirect(next_url)


@require_POST
def cart_update_view(request, product_id):
    """เพิ่ม/ลดจำนวนสินค้าในตะกร้า"""
    cart = Cart(request)
    action = request.POST.get('action')
    current_qty = cart.cart.get(str(product_id), 0)

    if action == 'increase':
        new_qty = current_qty + 1
    elif action == 'decrease':
        new_qty = current_qty - 1
    else:
        try:
            new_qty = int(request.POST.get('quantity', current_qty))
        except ValueError:
            new_qty = current_qty

    if new_qty <= 0:
        cart.remove(product_id)
        messages.info(request, 'ลบสินค้าออกจากตะกร้าแล้ว')
    else:
        success, message = cart.update(product_id, new_qty)
        if not success:
            messages.error(request, message)

    return redirect('cart:cart_detail')


@require_POST
def cart_remove_view(request, product_id):
    """ลบสินค้าออกจากตะกร้า"""
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, 'ลบสินค้าออกจากตะกร้าแล้ว')
    return redirect('cart:cart_detail')
