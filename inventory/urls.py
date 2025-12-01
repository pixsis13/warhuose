from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # صفحه اصلی شد داشبورد
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'), # لینک ویرایش
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
