from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    operation_type = models.ForeignKey(OperationType, on_delete=models.PROTECT, related_name="categories", verbose_name="Тип операции")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["operation_type__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "operation_type"],
                name="unique_category_per_operation_type",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.operation_type})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="subcategories", verbose_name="Категория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["category__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="unique_subcategory_per_category",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    created_at = models.DateField(default=timezone.localdate,verbose_name="Дата создания записи")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="records", verbose_name="Статус")
    operation_type = models.ForeignKey(OperationType, on_delete=models.PROTECT, related_name="records", verbose_name="Тип операции")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="records", verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name="records", verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)],verbose_name="Сумма")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return f"{self.created_at} — {self.type} — {self.amount} ₽"

    def clean(self) -> None:
        if self.category_id and self.type_id:
            if self.category.operation_type_id != self.type_id:
                raise ValidationError(
                    {
                        "category": "Категория не относится к выбранному типу операции."
                    }
                )

        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                raise ValidationError(
                    {
                        "subcategory": "Подкатегория не относится к выбранной категории."
                    }
                )