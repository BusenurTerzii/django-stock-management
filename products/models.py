from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ======================
# CATEGORY
# ======================
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ======================
# PRODUCT
# ======================
class Product(models.Model):
    name = models.CharField(max_length=150)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    sku = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.stock < 0:
            raise ValidationError({"stock": "Stok negatif olamaz."})

        if self.min_stock < 0:
            raise ValidationError({"min_stock": "Minimum stok negatif olamaz."})

    def __str__(self):
        return self.name


# ======================
# STOCK MOVEMENT
# ======================
class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ("in", "Giriş"),
        ("out", "Çıkış"),
    )

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="movements"
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_TYPES
    )

    quantity = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({"quantity": "Miktar 0'dan büyük olmalıdır."})

        if self.movement_type == "out" and self.product:
            if self.quantity > self.product.stock:
                raise ValidationError(
                    "Çıkış miktarı mevcut stoktan fazla olamaz."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # ValidationError burada zorunlu çalışır

        if self.movement_type == "in":
            self.product.stock += self.quantity
        elif self.movement_type == "out":
            self.product.stock -= self.quantity

        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"