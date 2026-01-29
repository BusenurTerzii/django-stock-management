import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject3.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "admin123"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("Superuser created")
else:
    print("Superuser already exists")