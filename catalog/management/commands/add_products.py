from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add products to database"

    def handle(self, *args, **kwargs):
        # Удаляем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем данные из фикстуры
        call_command("loaddata", "catalog_fixture.json")

        self.stdout.write(
            self.style.SUCCESS("Products and categories loaded from fixture")
        )
