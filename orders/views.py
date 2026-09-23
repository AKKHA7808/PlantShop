from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart

from .forms import CheckoutForm
from .models import Order, OrderDetail
from products.models import Product


@login_required
def checkout_view(request):
    """
    หน้ายืนยันคำสั่งซื้อ
    - GET: แสดงฟอร์มกรอกข้อมูลผู้รับ + สรุปตะกร้า
    - POST: ตรวจสอบสต็อกอีกครั้ง แล้วสร้าง Order + OrderDetail, ลด stock, ล้างตะกร้า
    """
    cart = Cart(request)

    cart_items = list(cart)

    if not cart_items:
        messages.warning(request, 'ตะกร้าของคุณว่างเปล่า กรุณาเลือกสินค้าก่อนทำการสั่งซื้อ')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                product_ids = [item['product'].id for item in cart_items]
                locked_products = Product.objects.select_for_update().filter(id__in=product_ids)
                product_map = {p.id: p for p in locked_products}

                for item in cart_items:
                    product = product_map.get(item['product'].id)
                    if not product:
                        messages.error(
                            request,
                            "มีสินค้าบางรายการไม่อยู่ในระบบแล้ว กรุณาตรวจสอบตะกร้าอีกครั้ง"
                        )
                        return redirect('cart:cart_detail')
                    
                    quantity = item['quantity']
                    if quantity > product.stock:
                        messages.error(
                            request,
                            f"สินค้า '{product.name}' มีสินค้าไม่เพียงพอ (คงเหลือ {product.stock} ชิ้น)"
                        )
                        return redirect('cart:cart_detail')

                order = form.save(commit=False)
                order.user = request.user
                
                total_price = sum(
                    product_map[item["product"].id].price * item["quantity"]
                    for item in cart_items
                )
                order.total_price = total_price
                order.save()

                for item in cart_items:
                    product = product_map[item['product'].id]
                    quantity = item['quantity']

                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    product.stock -= quantity
                    product.save(update_fields=['stock'])

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
