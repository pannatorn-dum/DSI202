from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product

from django.contrib import messages
from .models import Product

def homepage(request):
    if request.user.is_authenticated:
        messages.success(request, "ยินดีต้อนรับ")
        
    query = request.GET.get('q')
    
    # กรอง promotions ตรงนี้
    promotions = Product.objects.filter(is_promotion=True)[:10]
    
    if query:
        # กรอง products ที่ไม่ใช่ promotion และชื่อมีคำค้นหา
        products = Product.objects.filter(is_promotion=False, name__icontains=query)
    else:
        # ดึง products ที่ไม่ใช่ promotion จำกัด 10 รายการ
        products = Product.objects.filter(is_promotion=False)[:10]

    print("Products in homepage:", products)
    print("Promotion products:", promotions)

    return render(request, 'homepage.html', {
        'products': products,
        'promotions': promotions,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def cart_view(request):
    # ดึง cart จาก session หรือสร้างใหม่ถ้าไม่มี
    cart = request.session.get('cart', {})

    # สร้าง list รายการสินค้าใน cart
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.original_price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total_price += subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def add_to_cart(request, pk):
    # รับ POST หรือ GET แล้วเพิ่มสินค้าใน cart session
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'เพิ่มสินค้าลงตะกร้าแล้ว')
    return redirect('product_detail', pk=pk)


def payment(request):
    return render(request, 'payment.html')

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
