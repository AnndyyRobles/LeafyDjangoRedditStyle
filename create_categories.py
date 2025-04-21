import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from base.models import PlantCategory

# Crear las categorías iniciales
categories = [
    'Bulbs',
    'Herbs',
    'Vegetables',
    'Fruits'
]

for category_name in categories:
    category, created = PlantCategory.objects.get_or_create(name=category_name)
    if created:
        print(f'Categoría creada: {category_name}')
    else:
        print(f'Categoría ya existe: {category_name}')

print('\nCategorías en la base de datos:')
for category in PlantCategory.objects.all():
    print(f'- {category.name}')
