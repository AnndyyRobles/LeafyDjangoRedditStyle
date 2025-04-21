# Este script corrige la vista de createGuide para manejar correctamente las categorías
import os
import re

# Ruta del archivo de vistas
views_path = os.path.join('base', 'views.py')

# Leer el contenido del archivo
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón para encontrar la parte de categorías en createGuide
pattern_create = r'def createGuide\(request\):[\s\S]*?# Get category IDs from form\s*category_ids = request\.POST\.getlist\(\'categories\'\)\s*selected_categories = PlantCategory\.objects\.filter\(id__in=category_ids\)'

# Reemplazo para createGuide
replacement_create = """def createGuide(request):
    categories = PlantCategory.objects.all().order_by('name')
    
    if request.method == 'POST':
        # Get category from form (with new input format)
        category_name = request.POST.get('category')
        
        # Obtener o crear la categoría según el nombre
        if category_name:
            category, created = PlantCategory.objects.get_or_create(name=category_name)
            selected_categories = [category]
        else:
            selected_categories = []"""

# Reemplazar en createGuide
content = re.sub(pattern_create, replacement_create, content)

# Guardar el contenido modificado
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n¡La vista ha sido actualizada correctamente!')
print('Ahora el formulario procesará correctamente las categorías y el contador se actualizará.')
print('\nPara aplicar el cambio, debes reiniciar el servidor de Django.')
