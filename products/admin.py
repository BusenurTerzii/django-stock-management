from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.db.models import Sum
from django.urls import path
from django.shortcuts import redirect

from .models import Product, StockMovement, Category

admin.site.site_header = "Stok Yönetim Sistemi"
admin.site.site_title = "Stok Admin"
admin.site.index_title = "Genel Yönetim Paneli"
# ======================================================
# INLINE: STOCK MOVEMENT HISTORY
# ======================================================
class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    can_delete = False
    readonly_fields = (
        "movement_type",
        "quantity",
        "created_by",
        "created_at",
    )


# ======================================================
# FILTER: CRITICAL STOCK
# ======================================================
class CriticalStockFilter(SimpleListFilter):
    title = "Stok Durumu"
    parameter_name = "critical"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Kritik"),
            ("no", "Normal"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(stock__lte=models.F("min_stock"))
        if self.value() == "no":
            return queryset.filter(stock__gt=models.F("min_stock"))
        return queryset


# ======================================================
# PRODUCT ADMIN
# ======================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "product_count","total_stock")
    search_fields = ("name",)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Ürün Sayısı"

    def total_stock(self, obj):
        return obj.products.aggregate(
            total=Sum("stock")
        )["total"] or 0

    total_stock.short_description = "Toplam Stok"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "sku",
        "stock",
        "min_stock",
        "critical_stock",
        "is_active",
    )

    list_filter = (
        "is_active",
        "category",
    )
    search_fields = ("name", "sku")
    inlines = (StockMovementInline,)

    def critical_stock(self, obj):
        if not obj:
            return "-"

        if obj.stock <= obj.min_stock:
            return "🔴 KRİTİK"

        return "🟢 OK"


    critical_stock.short_description = "Stok Durumu"


# ======================================================
# STOCK MOVEMENT ADMIN
# ======================================================
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "movement_type",
        "quantity",
        "created_by",
        "created_at",
    )
