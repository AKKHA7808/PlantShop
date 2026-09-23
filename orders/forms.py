from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    """ฟอร์มกรอกข้อมูลผู้รับตอนยืนยันคำสั่งซื้อ"""

    class Meta:
        model = Order
        fields = ['receiver_name', 'phone', 'shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = True
