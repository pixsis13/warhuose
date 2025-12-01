from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام کالا")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    quantity = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name="حد هشدار موجودی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        return self.quantity * self.price

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
