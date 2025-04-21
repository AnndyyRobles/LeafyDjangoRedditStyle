# Script para corregir el manejo de categoru00edas en las vistas de guu00edas de plantas
import os
import re

# Ruta del archivo de vistas
views_path = os.path.join('base', 'views.py')

# Leer el contenido del archivo
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corregir la vista updateGuide
pattern_update = r"""        # Get category IDs from form\n        category_ids = request\.POST\.getlist\('categories'\)\n        selected_categories = PlantCategory\.objects\.filter\(id__in=category_ids\)"""

replacement_update = """        # Get category from form (with new input format)\n        category_name = request.POST.get('category')\n        \n        # Obtener o crear la categoru00eda segu00fan el nombre\n        if category_name:\n            category, created = PlantCategory.objects.get_or_create(name=category_name)\n            selected_categories = [category]\n        else:\n            selected_categories = []"""

# Reemplazar en updateGuide
content = re.sub(pattern_update, replacement_update, content)

# Guardar el contenido modificado
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n\u00a1Las vistas han sido actualizadas correctamente!')
print('\nAhora, creemos una funciu00f3n para recalcular las relaciones existentes entre guu00edas y categoru00edas...')

# Crear un script para recalcular las relaciones existentes
fix_script = """# fix_categories_count.py - Script para recalcular las relaciones de categoru00edas
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
    
    print(f"\nEncontradas {len(categories)} categoru00edas en total")
    
    # Obtener todas las guu00edas de plantas
    guides = PlantGuide.objects.all()
    print(f"Encontradas {len(guides)} guu00edas de plantas en total\n")
    
    # Mostrar el recuento actual de guu00edas por categoru00eda
    print("Recuento actual de guu00edas por categoru00eda:")
    for category in categories:
        print(f"- {category.name}: {category.plant_guides.count()} guu00edas")

if __name__ == '__main__':
    print("Iniciando recalculaciu00f3n de relaciones entre guu00edas y categoru00edas...")
    refresh_category_relationships()
    print("\nProceso completado. Si los conteos siguen siendo incorrectos,")
    print("reinicia el servidor Django e intenta crear una nueva guu00eda.")
"""

# Guardar el script adicional
with open('fix_categories_count.py', 'w', encoding='utf-8') as f:
    f.write(fix_script)

print('\nCreado script adicional fix_categories_count.py para diagnosticar la relaciu00f3n de categoru00edas.')
print('\n\nPARA SOLUCIONAR EL PROBLEMA SIGUE ESTOS PASOS:')
print('1. Reinicia el servidor Django')
print('2. Ejecuta "python fix_categories_count.py" para verificar las relaciones actuales')
print('3. Crea una nueva guu00eda o edita una existente seleccionando una categoru00eda')
print('4. Verifica que el contador se actualice correctamente ahora')
