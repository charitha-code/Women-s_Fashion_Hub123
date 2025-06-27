from django.shortcuts import render, redirect
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Home Page
def home(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'home.html', {
        'products': products,
        'cart': cart,
        'cart_count': cart_count
    })

# Add to Cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('home')

# View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=[int(pid) for pid in cart.keys()])
    cart_items = []

    for product in products:
        product_id_str = str(product.id)
        cart_items.append({
            'product': product,
            'quantity': cart[product_id_str],
            'total_price': product.price * cart[product_id_str]
        })

    return render(request, 'cart.html', {'cart_items': cart_items})

# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')

# Checkout Page with Razorpay Key
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=[int(pid) for pid in cart.keys()])
    cart_items = []
    total_price = 0

    for product in products:
        product_id_str = str(product.id)
        quantity = cart[product_id_str]
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

# Create Razorpay Order
@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        total_price = sum(
            Product.objects.get(id=int(pid)).price * quantity
            for pid, quantity in cart.items()
        )
        amount = int(total_price * 100)  # in paise

        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return JsonResponse({"order_id": order["id"], "amount": amount})

# Payment success
def payment_success(request):
    request.session['cart'] = {}  # Clear cart
    return render(request, 'payment_success.html')

# Signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Profile
@login_required
def profile(request):
    return render(request, 'profile.html')

# Filter by category (AJAX)
def category_products(request):
    category = request.GET.get('category', '')
    products = Product.objects.filter(category__iexact=category)
    product_list = [{"name": p.name, "price": p.price, "category": p.category} for p in products]
    return JsonResponse({"products": product_list})
