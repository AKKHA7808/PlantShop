from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_header = 'Botanica - ระบบจัดการหลังบ้าน'
admin.site.site_title = 'Botanica Admin'
admin.site.index_title = 'จัดการร้านค้า'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('products.urls')),
]

# ให้ Django serve ไฟล์รูปภาพสินค้าตอน Debug และบน Vercel
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'IS_VERCEL', False):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
