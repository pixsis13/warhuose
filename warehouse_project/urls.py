from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # مسیرهای لاگین و خروج پیش‌فرض جنگو
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # مسیر ثبت نام
    path('register/', inventory_views.register, name='register'),

    path('', include('inventory.urls')),
]
