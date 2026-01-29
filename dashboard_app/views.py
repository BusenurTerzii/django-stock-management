from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum, F

from products.models import Product, StockMovement
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django Stock Management System is Live")
def dashboard_view(request):
    user = request.user

    if not (user.is_superuser or user.groups.filter(name="StockManager").exists()):
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok")

    # Genel istatistikler
    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(
        total=Sum("stock")
    )["total"] or 0
    total_movements = StockMovement.objects.count()

    # Grafik verileri
    products = Product.objects.all()
    product_names = [p.name for p in products]
    product_stocks = [p.stock for p in products]
    product_min_stocks = [p.min_stock for p in products]

    critical_count = sum(1 for p in products if p.stock <= p.min_stock)
    normal_count = sum(1 for p in products if p.stock > p.min_stock)

    total_product_stock = sum(product_stocks)
    total_min_stock = sum(product_min_stocks)

    # Kritik ürünler
    critical_products = Product.objects.filter(
        stock__lte=F("min_stock"),
        is_active=True
    ).select_related("category")

    context = {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_movements": total_movements,

        "product_names": product_names,
        "product_stocks": product_stocks,
        "product_min_stocks": product_min_stocks,

        "critical_count": critical_count,
        "normal_count": normal_count,

        "total_product_stock": total_product_stock,
        "total_min_stock": total_min_stock,

        "critical_products": critical_products,
    }

    return render(request, "dashboard/dashboard.html", context)




