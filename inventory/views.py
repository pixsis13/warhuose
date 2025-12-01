from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Product
from .forms import ProductForm
from django.db.models import Q  # برای جستجوی پیشرفته‌تر


# 1. داشبورد: نمایش آمار
def dashboard(request):
    total_products = Product.objects.count()
    total_quantity = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    # محاسبه ارزش کل انبار (تعداد * قیمت)
    total_value = Product.objects.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()

    context = {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'inventory/dashboard.html', context)


# 3. ایجاد کالا
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'افزودن کالای جدید'})


# 4. ویرایش کالا (ویژگی جدید)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'ویرایش کالا'})


# 5. حذف کالا
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')

    if query:
        # جستجو هم در نام کالا و هم در توضیحات
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'inventory/product_list.html', {'products': products, 'query': query})
