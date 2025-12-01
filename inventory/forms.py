from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600 border-gray-300',
                'placeholder': 'نام دسته‌بندی جدید'
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'low_stock_threshold', 'description']

        COMMON_STYLE = 'w-full mt-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600 border-gray-300'

        widgets = {
            'name': forms.TextInput(attrs={'class': COMMON_STYLE}),
            'category': forms.Select(attrs={'class': COMMON_STYLE}),
            'quantity': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'price': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': COMMON_STYLE}),
            'description': forms.Textarea(attrs={'class': COMMON_STYLE, 'rows': 3}),
        }
