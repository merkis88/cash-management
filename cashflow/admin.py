from django.contrib import admin

from .models import (
    CashFlowRecord,
    Category,
    OperationType,
    Status,
    SubCategory,
)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "operation_type")
    list_filter = ("operation_type",)
    search_fields = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "status",
        "operation_type",
        "category",
        "subcategory",
        "amount",
    )
    list_filter = (
        "created_at",
        "status",
        "operation_type",
        "category",
        "subcategory",
    )
    search_fields = (
        "comment",
        "category__name",
        "subcategory__name",
    )
    date_hierarchy = "created_at"