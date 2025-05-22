from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product 
import promptpay
from promptpay import qrcode as pp
import qrcode, io, base64
from io import BytesIO

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


# ฟังก์ชันสร้าง QR Code พร้อมแปลงเป็น base64 string
def generate_promptpay_qr(amount, ref=None):
    phone_number = '0918259104'  # ใส่เบอร์พร้อมเพย์ของร้าน

    # ไลบรารีนี้รับเฉพาะเบอร์และ amount เท่านั้น (ไม่รองรับ ref/invoice)
    payload = pp.generate_payload(phone_number, amount)

    qr = qrcode.make(payload)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return qr_code_base64
def payment(request):
    cart = request.session.get('cart', {})

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

    # สมมุติสร้าง payment_ref จากเวลา/เลขสุ่ม (คุณอาจใช้ UUID หรือ model จริงในโปรเจกต์จริง)
    import random
    payment_ref = f"REF{random.randint(10000,99999)}"

    qr_code_base64 = generate_promptpay_qr(total_price, payment_ref)

    return render(request, 'payment.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'qr_code_base64': qr_code_base64,
        'promptpay_number': "0918259104",
        'payment_ref': payment_ref,
    })


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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ")
            return redirect('login')  # 'login' คือชื่อ url pattern ของหน้า login ของคุณ
        else:
            messages.error(request, "สมัครสมาชิกไม่สำเร็จ กรุณาลองใหม่")
    else:
        form = UserCreationForm()
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
