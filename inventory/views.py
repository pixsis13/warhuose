from django.shortcuts import get_object_or_404
from django.db.models import Q  # برای جستجوی پیشرفته‌تر
import csv
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, F, Count
from .models import Product, Category
from .forms import ProductForm, CategoryForm

# 1. داشبورد با داده‌های نمودار
def dashboard(request):
    total_products = Product.objects.count()
    total_quantity = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_value = Product.objects.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()

    # داده‌های نمودار دایره‌ای (دسته‌بندی‌ها)
    categories = Category.objects.annotate(item_count=Count('product'))
    cat_names = [c.name for c in categories]
    cat_counts = [c.item_count for c in categories]

    # داده‌های نمودار میله‌ای (5 کالای پر موجودی)
    top_products = Product.objects.all().order_by('-quantity')[:5]
    prod_names = [p.name for p in top_products]
    prod_quantities = [p.quantity for p in top_products]

    context = {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        # تبدیل داده‌ها به JSON برای جاوااسکریپت
        'chart_cat_names': json.dumps(cat_names),
        'chart_cat_counts': json.dumps(cat_counts),
        'chart_prod_names': json.dumps(prod_names),
        'chart_prod_quantities': json.dumps(prod_quantities),
    }
    return render(request, 'inventory/dashboard.html', context)

# 2. افزودن دسته‌بندی جدید
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list') # یا رایرکت به داشبورد
    return render(request, 'inventory/category_form.html', {'form': form})

# 3. گزارش‌گیری (CSV)
def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    response.write(u'\ufeff'.encode('utf8')) # BOM برای پشتیبانی از فارسی در اکسل

    writer = csv.writer(response)
    writer.writerow(['نام کالا', 'دسته‌بندی', 'تعداد', 'قیمت', 'ارزش کل'])

    products = Product.objects.all()
    for product in products:
        cat_name = product.category.name if product.category else "ندارد"
        writer.writerow([product.name, cat_name, product.quantity, product.price, product.total_value])

    return response

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
