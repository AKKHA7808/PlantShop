from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterForm


def register_view(request):
    """หน้าสมัครสมาชิก - เมื่อสำเร็จจะ login ให้อัตโนมัติ"""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'สมัครสมาชิกสำเร็จ ยินดีต้อนรับคุณ {user.first_name}')
            return redirect('products:home')
        else:
            messages.error(request, 'กรุณาตรวจสอบข้อมูลที่กรอกอีกครั้ง')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """หน้า Login - ใช้ AuthenticationForm มาตรฐานของ Django"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'เข้าสู่ระบบสำเร็จ ยินดีต้อนรับคุณ {form.get_user().first_name}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Username หรือ Password ไม่ถูกต้อง')
        return super().form_invalid(form)


def logout_view(request):
    """ออกจากระบบ"""
    logout(request)
    messages.info(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('products:home')
