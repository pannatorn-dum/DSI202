from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib import messages
from django.shortcuts import render

def homepage(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()[:4]  # แสดง 4 ชิ้นแรก

    return render(request, 'homepage.html', {'products': products})

def homepage(request):
    products = Product.objects.all()  # ดึงสินค้าทั้งหมด
    return render(request, 'homepage.html', {'Products': products})  # ส่งไปให้ template

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def homepage(request):
    if request.user.is_authenticated:
        # แสดงข้อความแจ้งเตือนเมื่อผู้ใช้ล็อกอินสำเร็จ
        messages.success(request, "ยินดีต้อนรับกลับค่ะ!")  # แสดงข้อความในหน้า homepage
    
    return render(request, 'homepage.html')  # เรนเดอร์หน้า homepage