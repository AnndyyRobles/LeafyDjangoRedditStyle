# fix_categories_count.py - Script para recalcular las relaciones de categoru00edas
import os
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

# Importar modelos despuu00e9s de configurar Django
from base.models import PlantGuide, PlantCategory

def refresh_category_relationships():
    # Obtener todas las categoru00edas
    categories = PlantCategory.objects.all()
    
    print(f"
Encontradas {len(categories)} categoru00edas en total")
    
    # Obtener todas las guu00edas de plantas
    guides = PlantGuide.objects.all()
    print(f"Encontradas {len(guides)} guu00edas de plantas en total
")
    
    # Mostrar el recuento actual de guu00edas por categoru00eda
    print("Recuento actual de guu00edas por categoru00eda:")
    for category in categories:
        print(f"- {category.name}: {category.plant_guides.count()} guu00edas")

if __name__ == '__main__':
    print("Iniciando recalculaciu00f3n de relaciones entre guu00edas y categoru00edas...")
    refresh_category_relationships()
    print("
Proceso completado. Si los conteos siguen siendo incorrectos,")
    print("reinicia el servidor Django e intenta crear una nueva guu00eda.")
