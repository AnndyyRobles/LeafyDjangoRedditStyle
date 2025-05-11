import os
import sys
# Agregar el directorio del proyecto al path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LeafyDjangoRedditStyle.settings')
import django
django.setup()

from base.models import PlantCategory

# Mapeo de categorías en inglés a español
category_mapping = {
    'Bulbs': 'Bulbos',
    'Fruits': 'Frutas',
    'Herbs': 'Hierbas',
    'Vegetables': 'Vegetales',
    'Flowers': 'Flores',
    'Trees': 'Árboles',
    'Succulents': 'Suculentas',
    'Vines': 'Enredaderas',
    'Greens': 'Verduras',
    'Roots': 'Raíces',
    'Berries': 'Bayas',
    'Grains': 'Granos',
    'Legumes': 'Legumbres',
    'Nuts': 'Frutos Secos'
}

# Actualizar categorías existentes
updated_count = 0
for category in PlantCategory.objects.all():
    if category.name in category_mapping:
        spanish_name = category_mapping[category.name]
        print(f"Actualizando: {category.name} -> {spanish_name}")
        category.name = spanish_name
        category.save()
        updated_count += 1

print(f"\nSe actualizaron {updated_count} categorías a español.")

# Verificar si hay categorías que faltan y crearlas
existing_categories = set(PlantCategory.objects.values_list('name', flat=True))
for spanish_name in category_mapping.values():
    if spanish_name not in existing_categories:
        print(f"Creando nueva categoría: {spanish_name}")
        PlantCategory.objects.create(name=spanish_name)

print("\nProceso completado.")
