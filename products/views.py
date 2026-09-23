from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home_view(request):
    """หน้าแรก: แสดงสินค้าล่าสุด 8 ชิ้นเป็นตัวอย่าง"""
    featured_products = Product.objects.all()[:8]
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
    })


def product_list_view(request):
    """
    หน้ารายการสินค้าทั้งหมด รองรับ:
    - ค้นหาจากชื่อสินค้า (?q=...)
    - กรองตามหมวดหมู่ (?category=<id>)
    ใช้ template เดียวกับหน้า Search Result
    """
    products = Product.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(name__icontains=query)

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


def product_detail_view(request, pk):
    """หน้ารายละเอียดสินค้า"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
