from django.contrib import admin
from django.urls import path, include  # ۱. اضافه کردن include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ۲. هدایت صفحه اصلی به اپلیکیشن انبارداری
    path('', include('inventory.urls')),
]
