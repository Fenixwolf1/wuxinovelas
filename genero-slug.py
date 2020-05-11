import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wuxi.settings')
django.setup()

from novelas.models import Generos
from slugify import slugify

generos_slug = Generos.objects.all()

for slug in generos_slug:
    slug.genero_slug = slugify(slug.genero)
    slug.save()