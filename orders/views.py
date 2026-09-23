from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderDetail


@login_required
def checkout_view(request):
    """
    หน้ายืนยันคำสั่งซื้อ
    - GET: แสดงฟอร์มกรอกข้อมูลผู้รับ + สรุปตะกร้า
    - POST: ตรวจสอบสต็อกอีกครั้ง แล้วสร้าง Order + OrderDetail, ลด stock, ล้างตะกร้า
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'ตะกร้าของคุณว่างเปล่า กรุณาเลือกสินค้าก่อนทำการสั่งซื้อ')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # ตรวจสอบสต็อกอีกครั้งก่อนตัดจริง เผื่อสต็อกเปลี่ยนไปหลังจากเพิ่มลงตะกร้า
            for item in cart:
                if item['quantity'] > item['product'].stock:
                    messages.error(
                        request,
                        f"สินค้า '{item['product'].name}' มีคงเหลือไม่พอ (เหลือ {item['product'].stock} ชิ้น)"
                    )
                    return redirect('cart:cart_detail')

            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = cart.get_total_price()
                order.save()

                for item in cart:
                    product = item['product']
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price,
                    )
                    # ลด stock สินค้า
                    product.stock -= item['quantity']
                    product.save()

                cart.clear()

            messages.success(request, 'สั่งซื้อสำเร็จ! ขอบคุณที่ใช้บริการสวนใบไม้')
            return redirect('orders:order_success', order_id=order.id)
    else:
        # เติมข้อมูลผู้ใช้ให้อัตโนมัติจากโปรไฟล์ (ถ้ามี)
        form = CheckoutForm(initial={
            'receiver_name': request.user.first_name or request.user.username,
            'phone': request.user.phone,
            'shipping_address': request.user.address,
        })

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_success_view(request, order_id):
    """หน้าแจ้งผลสำเร็จหลังสั่งซื้อ"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    """หน้าประวัติการสั่งซื้อ - แสดงเฉพาะคำสั่งซื้อของผู้ใช้ที่ login เท่านั้น"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    """
    หน้ารายละเอียดคำสั่งซื้อ
    filter(user=request.user) ป้องกันไม่ให้ลูกค้าคนอื่นดู order ที่ไม่ใช่ของตัวเองได้
    (ถ้าไม่ใช่เจ้าของ order จะได้ 404 แทนที่จะเห็นข้อมูลของคนอื่น)
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
