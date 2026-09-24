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
            
        # เปลี่ยนข้อความช่วยเหลือเป็นภาษาไทย
        if 'username' in self.fields:
            self.fields['username'].label = 'ชื่อผู้ใช้งาน'
            self.fields['username'].help_text = 'ความยาวไม่เกิน 150 ตัวอักษร ใช้ได้เฉพาะตัวอักษร, ตัวเลข และ @/./+/-/_'
        if 'password1' in self.fields:
            self.fields['password1'].label = 'รหัสผ่าน'
            self.fields['password1'].help_text = 'รหัสผ่านต้องไม่สั้นเกินไป และไม่ควรใช้ข้อมูลส่วนตัวที่เดาง่าย'
        if 'password2' in self.fields:
            self.fields['password2'].label = 'ยืนยันรหัสผ่าน'
            self.fields['password2'].help_text = 'กรอกรหัสผ่านอีกครั้งเพื่อยืนยันความถูกต้อง'

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
