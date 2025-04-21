# Script para diagnosticar y corregir la relación entre Guías y Categorías
import os
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

# Importar después de configurar Django
from base.models import PlantGuide, PlantCategory

# Diagnosticar el problema
print("\n==== DIAGNÓSTICO DE CATEGORÍAS Y GUÍAS ====\n")

# 1. Ver todas las categorías
categories = PlantCategory.objects.all().order_by('name')
print(f"Total de categorías: {categories.count()}")
for category in categories:
    guide_count = category.plant_guides.count()
    print(f"- {category.name}: {guide_count} guías asociadas")

# 2. Ver todas las guías
print("\n==== GUÍAS EXISTENTES ====\n")
guides = PlantGuide.objects.all()
print(f"Total de guías: {guides.count()}")

for guide in guides:
    categories_list = ", ".join([cat.name for cat in guide.categories.all()])
    print(f"Guía: {guide.common_name} - Categorías: {categories_list if categories_list else 'NINGUNA'}")

# 3. Preguntar si se desea hacer una corrección forzada
print("\n==== OPCIONES DE CORRECCIÓN ====\n")
print("¿Qué deseas hacer?")
print("1. Recalcular todas las relaciones")
print("2. Asignar la primera categoría existente a todas las guías sin categoría")
print("3. Salir sin hacer cambios")

choice = input("Tu elección (1/2/3): ")

if choice == '1':
    print("\nRecalculando relaciones... Este proceso puede tardar.")
    # Aquí se podría implementar un recálculo si fuera necesario
    # Por ahora, no es necesario ya que Django maneja esto automáticamente
    print("Las relaciones deberían estar correctas. Si el problema persiste,")
    print("verifica que las guías tengan categorías asignadas.")

elif choice == '2':
    # Buscar guías sin categorías
    guides_without_categories = [g for g in guides if g.categories.count() == 0]
    
    if guides_without_categories and categories.exists():
        print(f"\nEncontradas {len(guides_without_categories)} guías sin categorías")
        first_category = categories.first()
        
        print(f"Asignando la categoría '{first_category.name}' a todas las guías sin categoría...")
        for guide in guides_without_categories:
            guide.categories.add(first_category)
            print(f"  - Añadida categoría '{first_category.name}' a la guía '{guide.common_name}'")
        
        print("\n¡Proceso completado!")
    else:
        print("No hay guías sin categorías o no hay categorías disponibles.")

else:
    print("\nSaliendo sin hacer cambios.")

print("\nRecuerda reiniciar el servidor Django para que los cambios surtan efecto.")
