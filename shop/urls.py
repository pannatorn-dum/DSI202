from django.contrib import admin
from django.urls import path
from shopapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
        # URL สำหรับล็อกอิน
    path('login/', auth_views.LoginView.as_view(), name='account_login'),
    # URL สำหรับออกจากระบบ
    path('logout/', auth_views.LogoutView.as_view(), name='account_logout'),
    # URL สำหรับหน้าแรก
    path('', views.homepage, name='homepage'),
]

# ✅ ให้ Django เสิร์ฟ media files (เช่น รูปภาพ)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
