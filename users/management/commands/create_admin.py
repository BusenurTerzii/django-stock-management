import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject3.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
email = "admin@admin.com"
password = "Admin123!"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")