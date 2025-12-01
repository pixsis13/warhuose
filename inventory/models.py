from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    def __str__(self): return self.name

class Product(models.Model):
    # لیست واحدهای اندازه‌گیری
    UNIT_CHOICES = [
        ('num', 'عدد'),
        ('kg', 'کیلوگرم'),
        ('g', 'گرم'),
        ('ltr', 'لیتر'),
        ('m', 'متر'),
        ('box', 'جعبه/بسته'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام کالا")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    
    quantity = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='num', verbose_name="واحد")
    
    # قیمت اختیاری شد
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)", null=True, blank=True)
    
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name="حد هشدار موجودی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        # اگر قیمت وارد نشده بود، ارزش را صفر در نظر بگیر
        if self.price:
            return self.quantity * self.price
        return 0

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
