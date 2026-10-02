"""
Django settings for plantshop project.
โปรเจกต์ร้านขายต้นไม้และดอกไม้ประดับออนไลน์ (สำหรับใช้ในงานเรียน)
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
# หมายเหตุ: ใน production จริงควรเก็บ SECRET_KEY ไว้ใน environment variable
# เช่น: import os; SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
SECRET_KEY = 'django-insecure-change-this-key-for-production-usage'

# ควรใช้ os.environ.get('DEBUG', 'True') == 'True' ใน production
DEBUG = True

# ควรระบุโดเมนจริงใน production เช่น ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
ALLOWED_HOSTS = ['*']

# อนุญาตให้ Ngrok ส่งข้อมูล POST ได้โดยไม่ติด 403 CSRF Error
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok-free.dev',
    'https://*.ngrok.io',
    'https://*.ngrok.app',
    'https://*.ngrok.dev',
]

# --- Applications ---
INSTALLED_APPS = [
    'jazzmin',  # ต้องอยู่บนสุดของ INSTALLED_APPS เสมอ
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # แอปของโปรเจกต์
    'accounts',
    'products',
    'cart',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plantshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # เก็บ template รวมไว้ที่ templates/ ระดับโปรเจกต์ + template ในแต่ละแอป
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ทำให้ทุกหน้าเห็นจำนวนสินค้าในตะกร้าได้ (ใช้ใน Navbar)
                'cart.context_processors.cart_summary',
            ],
        },
    },
]

WSGI_APPLICATION = 'plantshop.wsgi.application'

# --- Database (SQLite) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Custom User model ---
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# --- Static & Media files ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Login redirects ---
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'products:home'
LOGOUT_REDIRECT_URL = 'products:home'

# --- Jazzmin Admin Settings ---
JAZZMIN_SETTINGS = {
    "site_title": "ระบบหลังบ้าน สวนใบไม้",
    "site_header": "สวนใบไม้ Admin",
    "site_brand": "🌿 PlantShop",
    "welcome_sign": "ยินดีต้อนรับสู่ระบบหลังบ้าน สวนใบไม้",
    "search_model": ["accounts.User", "products.Product", "orders.Order"],
    "show_ui_builder": False,
    "topmenu_links": [
        {"name": "หน้าแรกเว็บไซต์",  "url": "products:home", "permissions": ["accounts.view_user"]},
    ],
    "icons": {
        "accounts.User": "fas fa-users",
        "products.Category": "fas fa-tags",
        "products.Product": "fas fa-leaf",
        "orders.Order": "fas fa-shopping-cart",
        "orders.OrderDetail": "fas fa-box",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}
