from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'low_stock_threshold', 'description']

        # استایل مشترک برای تمام اینپوت‌ها
        COMMON_STYLE = 'w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200'

        widgets = {
            'name': forms.TextInput(attrs={'class': COMMON_STYLE, 'placeholder': 'مثال: لپ‌تاپ ایسوس'}),
            'category': forms.Select(attrs={'class': COMMON_STYLE}),
            'quantity': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'price': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'description': forms.Textarea(attrs={'class': COMMON_STYLE, 'rows': 3}),
        }
