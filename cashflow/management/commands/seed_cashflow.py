from django.core.management.base import BaseCommand

from cashflow.models import Category, OperationType, Status, SubCategory


class Command(BaseCommand):
    help = "Seed initial cashflow reference data"

    def handle(self, *args, **options):
        statuses = ["Бизнес", "Личное", "Налог"]

        for status_name in statuses:
            Status.objects.get_or_create(name=status_name)

        replenishment, _ = OperationType.objects.get_or_create(name="Пополнение")
        write_off, _ = OperationType.objects.get_or_create(name="Списание")

        infrastructure, _ = Category.objects.get_or_create(name="Инфраструктура",operation_type=write_off)

        marketing, _ = Category.objects.get_or_create(name="Маркетинг", operation_type=write_off)

        for subcategory_name in ["VPS", "Proxy"]:
            SubCategory.objects.get_or_create(name=subcategory_name,category=infrastructure)

        for subcategory_name in ["Farpost", "Avito"]:
            SubCategory.objects.get_or_create(name=subcategory_name,category=marketing)

        self.stdout.write(
            self.style.SUCCESS("Cashflow reference data seeded successfully.")
        )