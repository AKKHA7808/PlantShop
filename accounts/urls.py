from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/demo-admin/', views.demo_admin_login_view, name='demo_admin_login'),
    path('logout/', views.logout_view, name='logout'),
]
