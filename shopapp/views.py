from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product

def homepage(request):
    if request.user.is_authenticated:
        messages.success(request, "ยินดีต้อนรับ")
        
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()[:4]

    print("Products in homepage:", products)  # เช็คใน terminal/log

    return render(request, 'homepage.html', {'products': products})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    return render(request, 'account/login.html')

def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('homepage')
    return render(request, 'account/signup.html', {'form': form})

def forgot_password_view(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            email_template_name='accounts/password_reset_email.html',  # ถ้ามี
        )
        return redirect('password_reset_done')
    return render(request, 'account/forgot_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')
