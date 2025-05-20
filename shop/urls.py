from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shopapp import views  # ✅ ต้อง import views จาก shopapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopapp.urls')),  # หน้า homepage, product list, etc.
    
    # 🔻 Custom authentication views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
