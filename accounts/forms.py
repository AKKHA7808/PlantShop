from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """
    ฟอร์มสมัครสมาชิก ต่อยอดจาก UserCreationForm ของ Django
    (จัดการเรื่อง password hashing และ validation ให้อัตโนมัติ)
    """
    first_name = forms.CharField(label='ชื่อ', max_length=150, required=True)
    email = forms.EmailField(label='อีเมล', required=True)
    phone = forms.CharField(label='เบอร์โทรศัพท์', max_length=15, required=True)
    address = forms.CharField(label='ที่อยู่', widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ใส่ class 'form-control' ให้ทุก field เพื่อให้หน้าตาตรงกับ Bootstrap 5
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('อีเมลนี้ถูกใช้งานแล้ว')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user
