from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm
from .models import Category, Product, Order, OrderItem

def _cart(request):
    return request.session.get("cart", {})

def _cart_details(request):
    cart_data, total, count = [], Decimal("0.00"), 0
    for pid, qty in _cart(request).items():
        product = Product.objects.filter(pk=pid, is_active=True).first()
        if product and int(qty) > 0:
            subtotal = product.price * int(qty)
            cart_data.append({"product": product, "quantity": int(qty), "subtotal": subtotal})
            total += subtotal
            count += int(qty)
    return cart_data, total, count

def catalog(request):
    products = Product.objects.filter(is_active=True, stock__gt=0).select_related("category")
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category.isdigit():
        products = products.filter(category_id=int(category))
    cart_items, cart_total, cart_count = _cart_details(request)
    return render(request, "store/catalog.html", {
        "products": products, "categories": Category.objects.all(), "q": q,
        "selected_category": category, "cart_count": cart_count,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    alternatives = Product.objects.filter(
        swap_group=product.swap_group, is_active=True, stock__gt=0, price__lt=product.price
    ).exclude(pk=product.pk).order_by("price") if product.swap_group else Product.objects.none()
    return render(request, "store/product_detail.html", {"product": product, "alternatives": alternatives})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("catalog")
    cart = _cart(request)
    current = int(cart.get(str(product_id), 0))
    if current >= product.stock:
        messages.warning(request, "You already added all available stock.")
    else:
        cart[str(product_id)] = current + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} added to your basket.")
    return redirect(request.POST.get("next") or "catalog")

def cart(request):
    items, total, count = _cart_details(request)
    return render(request, "store/cart.html", {"items": items, "total": total, "count": count})

@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    cart = _cart(request)
    if qty <= 0:
        cart.pop(str(product_id), None)
    elif qty <= product.stock:
        cart[str(product_id)] = qty
    else:
        messages.error(request, f"Only {product.stock} units of {product.name} are available.")
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, product_id):
    cart = _cart(request)
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
@require_POST
def checkout(request):
    cart = _cart(request)
    if not cart:
        messages.info(request, "Your basket is empty.")
        return redirect("catalog")
    with transaction.atomic():
        products = {str(p.pk): p for p in Product.objects.select_for_update().filter(
            pk__in=[int(k) for k in cart.keys()], is_active=True
        )}
        total = Decimal("0.00")
        checked = []
        for pid, raw_qty in cart.items():
            product = products.get(pid)
            qty = int(raw_qty)
            if not product or qty < 1 or product.stock < qty:
                messages.error(request, "Stock changed while you were shopping. Please review your basket.")
                return redirect("cart")
            total += product.price * qty
            checked.append((product, qty))
        order = Order.objects.create(user=request.user, total=total)
        for product, qty in checked:
            OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=product.price)
            product.stock -= qty
            product.save(update_fields=["stock"])
    request.session["cart"] = {}
    messages.success(request, f"Order #{order.pk} placed successfully! (Demo checkout; no payment collected.)")
    return redirect("orders")

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "store/orders.html", {"orders": user_orders})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome to SmartBasket!")
            return redirect("catalog")
    else:
        form = SignUpForm()
    return render(request, "store/auth.html", {"form": form, "title": "Create account", "button": "Sign up"})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("catalog")
    else:
        form = AuthenticationForm(request)
    return render(request, "store/auth.html", {"form": form, "title": "Welcome back", "button": "Log in"})

def logout_view(request):
    logout(request)
    return redirect("catalog")
