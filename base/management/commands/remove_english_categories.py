from django.core.management.base import BaseCommand
from base.models import PlantCategory

class Command(BaseCommand):
    help = 'Remove English plant categories and the category "Otro"'

    def handle(self, *args, **options):
        # Lista de categorías en inglés a eliminar
        english_categories = [
            'Bulbs', 'Fruits', 'Herbs', 'Vegetables'
        ]

        # Eliminar categorías en inglés
        for category_name in english_categories:
            try:
                category = PlantCategory.objects.get(name=category_name)
                category.delete()
                self.stdout.write(self.style.SUCCESS(f'Eliminada categoría en inglés: {category_name}'))
            except PlantCategory.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No se encontró la categoría: {category_name}'))

        # Eliminar categoría 'Otro' en español
        try:
            otro_category = PlantCategory.objects.get(name='Otro')
            otro_category.delete()
            self.stdout.write(self.style.SUCCESS('Eliminada categoría: Otro'))
        except PlantCategory.DoesNotExist:
            self.stdout.write(self.style.WARNING('No se encontró la categoría: Otro'))

        self.stdout.write(self.style.SUCCESS('Eliminación de categorías completada.'))
