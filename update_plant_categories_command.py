from django.core.management.base import BaseCommand
from base.models import PlantCategory

class Command(BaseCommand):
    help = 'Update plant categories to Spanish'

    def handle(self, *args, **options):
        # Mapeo de categorías de plantas de inglés a español
        category_mapping = {
            'Fruit': 'Fruta',
            'Vegetable': 'Vegetal',
            'Herb': 'Hierba',
            'Flower': 'Flor',
            'Tree': 'Árbol',
            'Shrub': 'Arbusto',
            'Succulent': 'Suculenta',
            'Fern': 'Helecho',
            'Grass': 'Césped',
            'Vine': 'Enredadera',
            'Other': 'Otro'
        }

        # Actualizar categorías existentes
        for old_name, new_name in category_mapping.items():
            try:
                category = PlantCategory.objects.get(name=old_name)
                category.name = new_name
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Actualizada categoría: {old_name} -> {new_name}'))
            except PlantCategory.DoesNotExist:
                # Si la categoría no existe, crearla
                PlantCategory.objects.create(name=new_name)
                self.stdout.write(self.style.SUCCESS(f'Creada categoría: {new_name}'))

        self.stdout.write(self.style.SUCCESS('Actualización de categorías completada.'))
