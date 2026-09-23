# สวนใบไม้ (Plant Shop) — โปรเจกต์เต็ม (Phase 1–5)

ระบบร้านขายต้นไม้และดอกไม้ประดับออนไลน์ พัฒนาด้วย Django + Bootstrap 5 + SQLite
เหมาะสำหรับโปรเจกต์นักศึกษาระดับปริญญาตรี เน้นความเรียบง่าย อ่านโค้ดง่าย

## วิธีรัน (รันในเครื่องของคุณเอง — sandbox ที่ใช้เขียนโค้ดนี้ไม่มีอินเทอร์เน็ต จึงติดตั้ง/รันทดสอบจริงให้ไม่ได้)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # สร้างบัญชี Admin

python manage.py runserver
```

เปิดเบราว์เซอร์ที่ http://127.0.0.1:8000/
เข้า Django Admin ที่ http://127.0.0.1:8000/admin/

## โครงสร้างโปรเจกต์
```
plantshop/
├── manage.py
├── requirements.txt
├── plantshop/          # settings.py, urls.py (รวม url ทุกแอป), wsgi.py, asgi.py
├── accounts/           # Custom User (username, first_name, email, phone, address)
│   ├── models.py       # User(AbstractUser)
│   ├── forms.py        # RegisterForm
│   ├── views.py        # register_view, CustomLoginView, logout_view
│   └── templates/accounts/  # register.html, login.html
├── products/           # Category, Product + หน้าสำหรับลูกค้า
│   ├── models.py       # Category, Product
│   ├── admin.py        # จัดการสินค้า/หมวดหมู่ผ่าน Django Admin
│   ├── views.py        # home, product_list (รองรับค้นหา+กรองหมวดหมู่), product_detail
│   └── templates/products/  # home, product_list (ใช้เป็น search result ด้วย), product_detail, _product_card (partial)
├── cart/                # ตะกร้าสินค้าแบบ Session-based (ไม่ใช้ Database)
│   ├── cart.py          # class Cart: add/update/remove/clear/get_total_price
│   ├── views.py         # cart_detail, cart_add, cart_update, cart_remove
│   ├── context_processors.py  # cart_count ใช้แสดงเลขในตะกร้าที่ Navbar
│   └── templates/cart/cart_detail.html
└── orders/              # Order, OrderDetail + checkout
    ├── models.py        # Order (status: pending/shipping/completed/cancelled), OrderDetail
    ├── forms.py         # CheckoutForm (receiver_name, phone, shipping_address)
    ├── admin.py         # ดู/เปลี่ยนสถานะคำสั่งซื้อ พร้อม inline รายการสินค้า
    ├── views.py         # checkout (สร้าง order + ลด stock + ล้างตะกร้า), order_success,
    │                    # order_history (เห็นเฉพาะของตัวเอง), order_detail (กันดู order คนอื่น)
    └── templates/orders/  # checkout, order_success, order_history, order_detail
```

## Database Models และความสัมพันธ์
- `User` (accounts) 1 — N `Order` (orders)
- `Category` (products) 1 — N `Product` (products)
- `Order` 1 — N `OrderDetail`
- `Product` 1 — N `OrderDetail`

## สรุปแต่ละ Phase ที่ทำแล้ว
- **Phase 1**: Django project, apps, SQLite, static/media, Custom User (phone/address), register/login/logout, base template + Bootstrap 5 + Navbar
- **Phase 2**: Category/Product models, จัดการผ่าน Django Admin, หน้า List/Detail/ค้นหา/กรองหมวดหมู่สำหรับลูกค้า, แสดง "สินค้าหมด" เมื่อ stock=0
- **Phase 3**: ตะกร้าสินค้าแบบ Session (`cart/cart.py`) — เพิ่ม/ลด/ลบ/ดูราคารวม พร้อมตรวจสอบไม่ให้เกิน stock และต้องมากกว่า 0
- **Phase 4**: Checkout → สร้าง `Order` + `OrderDetail`, ลด stock, ล้างตะกร้า (ทำใน `transaction.atomic()` เพื่อความถูกต้องของข้อมูล), ประวัติ/รายละเอียดคำสั่งซื้อ (เห็นเฉพาะของตัวเองเท่านั้น ผ่าน `filter(user=request.user)`)
- **Phase 5**: ใช้ Django Admin เป็นหลังบ้านหลัก ตั้งค่า `list_display`, `list_filter`, `search_fields`, `list_editable` ให้จัดการสินค้า/หมวดหมู่/คำสั่งซื้อได้สะดวก พร้อมเปลี่ยนสถานะคำสั่งซื้อได้จากหน้ารายการ

## Security ที่ใช้ (มาตรฐาน Django)
- CSRF Protection: ทุกฟอร์ม (`{% csrf_token %}`)
- Password Hashing: ผ่าน `UserCreationForm` / Django Auth
- Login Required: `@login_required` ในทุก view ของ orders
- Permission/Ownership: `order_detail_view`/`order_history_view` filter ด้วย `user=request.user` เท่านั้น ลูกค้าดู order คนอื่นไม่ได้ (จะได้ 404)
- Admin-only functions อยู่ใน Django Admin ซึ่งต้อง `is_staff` เท่านั้นจึงเข้าได้

## Checklist การทดสอบ (ทำตามลำดับหลัง pip install + migrate)
1. [ ] `python manage.py migrate` ไม่มี error
2. [ ] `python manage.py runserver` รันได้ ไม่มี URL/Template error (เข้าทุกหน้าจาก Navbar ได้)
3. [ ] สมัครสมาชิก → login อัตโนมัติ → logout ได้
4. [ ] `createsuperuser` แล้วเข้า `/admin/` เพิ่ม Category และ Product ได้ (ลองใส่ stock=0 ดูว่าหน้าเว็บขึ้น "สินค้าหมด")
5. [ ] หน้า Products: ค้นหาชื่อสินค้า และกรองตามหมวดหมู่ได้ถูกต้อง
6. [ ] เพิ่มสินค้าลงตะกร้า, เพิ่ม/ลดจำนวน, ลบสินค้า, ราคารวมคำนวณถูกต้อง
7. [ ] ลองเพิ่มจำนวนเกิน stock → ระบบต้องแจ้งเตือนและไม่ให้เพิ่ม
8. [ ] Checkout กรอกข้อมูลผู้รับ → สั่งซื้อสำเร็จ → เช็คใน Admin ว่า stock สินค้าลดลงถูกต้อง และตะกร้าถูกล้าง
9. [ ] ดูประวัติคำสั่งซื้อ (Order History) และรายละเอียด (Order Detail)
10. [ ] ล็อกอินด้วยบัญชีอื่นแล้วลองเข้า URL order detail ของบัญชีแรกตรง ๆ → ต้องเข้าไม่ได้ (404)
11. [ ] ใน Admin: เปลี่ยนสถานะคำสั่งซื้อ (pending → shipping → completed)

หากพบปัญหาใด ๆ ระหว่างทดสอบ แจ้งรายละเอียด error กลับมาได้เลย จะช่วยแก้ไขให้ทันที
