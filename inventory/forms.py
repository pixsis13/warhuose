from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category

# فرم ثبت‌نام کاربر جدید
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="ایمیل (اختیاری)")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    # استایل دهی به فرم‌های پیش‌فرض جنگو
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        COMMON_STYLE = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600 border-gray-300 mt-1'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = COMMON_STYLE

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'unit', 'price', 'low_stock_threshold', 'description']
        
        COMMON_STYLE = 'w-full mt-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600 border-gray-300'

        widgets = {
            'name': forms.TextInput(attrs={'class': COMMON_STYLE}),
            'category': forms.Select(attrs={'class': COMMON_STYLE}),
            'quantity': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'unit': forms.Select(attrs={'class': COMMON_STYLE}), # ویجت انتخاب واحد
            'price': forms.NumberInput(attrs={'class': COMMON_STYLE, 'placeholder': 'خالی بگذارید اگر قیمت ندارد'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'description': forms.Textarea(attrs={'class': COMMON_STYLE, 'rows': 3}),
        }
