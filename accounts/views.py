from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import RegisterForm

User = get_user_model()


def register_view(request):
    """หน้าสมัครสมาชิก - เมื่อสำเร็จจะ login ให้อัตโนมัติ"""
    if request.user.is_authenticated:
        return redirect('products:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            display_name = user.first_name or user.username
            messages.success(request, f'สมัครสมาชิกสำเร็จ ยินดีต้อนรับคุณ {display_name}')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_demo_admin'] = settings.DEBUG
        return context

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        if self.request.user.is_staff:
            return reverse_lazy('admin:index')
        return super().get_success_url()

    def form_valid(self, form):
        user = form.get_user()
        display_name = user.first_name or user.username
        messages.success(self.request, f'เข้าสู่ระบบสำเร็จ ยินดีต้อนรับคุณ {display_name}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Username หรือ Password ไม่ถูกต้อง')
        return super().form_invalid(form)


@require_POST
def demo_admin_login_view(request):
    """เข้าสู่ระบบ Admin อัตโนมัติสำหรับทดสอบ (เปิดใช้งานเฉพาะตอน DEBUG=True)"""
    if not settings.DEBUG:
        raise Http404()

    admin_user = (
        User.objects.filter(is_superuser=True, is_active=True).order_by('id').first()
        or User.objects.filter(is_staff=True, is_active=True).order_by('id').first()
    )
    if not admin_user:
        messages.error(request, 'ไม่พบบัญชี Admin ในระบบ กรุณาสร้างด้วยคำสั่ง createsuperuser')
        return redirect('accounts:login')

    login(request, admin_user, backend='django.contrib.auth.backends.ModelBackend')
    display_name = admin_user.first_name or admin_user.username
    messages.success(request, f'เข้าสู่ระบบ Admin ทดสอบสำเร็จ ({display_name})')
    return redirect('admin:index')


@require_POST
def logout_view(request):
    """ออกจากระบบ"""
    logout(request)
    messages.info(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('products:home')
