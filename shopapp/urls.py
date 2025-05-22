from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('payment/', views.payment, name='payment'),
    # เพิ่มบรรทัดนี้เพื่อชี้ไปยัง login view ของคุณเอง
    path('login/', views.login_view, name='login'),
    # allauth URLs สำหรับ login, logout, signup, password reset
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup_view, name='account_signup'),
]
