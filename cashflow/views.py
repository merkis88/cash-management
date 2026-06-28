from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (CashFlowRecordFilterForm, CashFlowRecordForm, CategoryForm, OperationTypeForm, StatusForm, SubCategoryForm)
from .models import (CashFlowRecord, Category, OperationType, Status, SubCategory)

def record_list(request):
    """
    Home page.
    Display a table of cash flow records and applies filters.
    """

    records = CashFlowRecord.objects.select_related(
        "status",
        "operation_type",
        "category",
        "subcategory",
    ).all()

    filter_form = CashFlowRecordFilterForm(request.GET or None)

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get("date_from")
        date_to = filter_form.cleaned_data.get("date_to")
        status = filter_form.cleaned_data.get("status")
        operation_type = filter_form.cleaned_data.get("operation_type")
        category = filter_form.cleaned_data.get("category")
        subcategory = filter_form.cleaned_data.get("subcategory")

        if date_from:
            records = records.filter(created_at__gte=date_from)

        if date_to:
            records = records.filter(created_at__lte=date_to)

        if status:
            records = records.filter(status=status)

        if operation_type:
            records = records.filter(operation_type=operation_type)

        if category:
            records = records.filter(category=category)

        if subcategory:
            records = records.filter(subcategory=subcategory)

    context = {
        "records": records,
        "filter_form": filter_form,
    }

    return render(request, "cashflow/record_list.html", context)


def record_create(request):

    if request.method == "POST":
        form = CashFlowRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Запись ДДС успешно создана.")
            return redirect("cashflow:record_list")
    else:
        form = CashFlowRecordForm()

    context = {
        "form": form,
        "title": "Создание записи ДДС",
        "button_text": "Создать",
    }

    return render(request, "cashflow/record_form.html", context)


def record_update(request, pk):

    record = get_object_or_404(CashFlowRecord, pk=pk)

    if request.method == "POST":
        form = CashFlowRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Запись ДДС успешно обновлена.")
            return redirect("cashflow:record_list")
    else:
        form = CashFlowRecordForm(instance=record)

    context = {
        "form": form,
        "record": record,
        "title": "Редактирование записи ДДС",
        "button_text": "Сохранить",
    }

    return render(request, "cashflow/record_form.html", context)


def record_delete(request, pk):

    record = get_object_or_404(CashFlowRecord, pk=pk)

    if request.method == "POST":
        record.delete()
        messages.success(request, "Запись ДДС успешно удалена.")
        return redirect("cashflow:record_list")

    context = {
        "record": record,
    }

    return render(request, "cashflow/record_confirm_delete.html", context)


def categories_by_operation_type(request):

    operation_type_id = request.GET.get("operation_type_id")

    categories = Category.objects.none()

    if operation_type_id:
        categories = Category.objects.filter(
            operation_type_id=operation_type_id
        ).order_by("name")

    data = [
        {
            "id": category.id,
            "name": category.name,
        }
        for category in categories
    ]

    return JsonResponse({"results": data})


def subcategories_by_category(request):

    category_id = request.GET.get("category_id")

    subcategories = SubCategory.objects.none()

    if category_id:
        subcategories = SubCategory.objects.filter(
            category_id=category_id
        ).order_by("name")

    data = [
        {
            "id": subcategory.id,
            "name": subcategory.name,
        }
        for subcategory in subcategories
    ]

    return JsonResponse({"results": data})

REFERENCE_CONFIG = {
    "statuses": {
        "model": Status,
        "form": StatusForm,
        "title": "Статусы",
        "single_title": "статус",
    },
    "operation-types": {
        "model": OperationType,
        "form": OperationTypeForm,
        "title": "Типы операций",
        "single_title": "тип операции",
    },
    "categories": {
        "model": Category,
        "form": CategoryForm,
        "title": "Категории",
        "single_title": "категорию",
    },
    "subcategories": {
        "model": SubCategory,
        "form": SubCategoryForm,
        "title": "Подкатегории",
        "single_title": "подкатегорию",
    },
}


def get_reference_config(reference_type):
    config = REFERENCE_CONFIG.get(reference_type)

    if config is None:
        raise PermissionDenied("Неизвестный тип справочника.")

    return config


def reference_list(request):
    context = {
        "statuses": Status.objects.all(),
        "operation_types": OperationType.objects.all(),
        "categories": Category.objects.select_related("operation_type").all(),
        "subcategories": SubCategory.objects.select_related("category").all(),
    }

    return render(request, "cashflow/reference_list.html", context)


def reference_create(request, reference_type):
    config = get_reference_config(reference_type)
    form_class = config["form"]

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Справочник успешно обновлён.")
            return redirect("cashflow:reference_list")
    else:
        form = form_class()

    context = {
        "form": form,
        "title": f"Добавить {config['single_title']}",
        "button_text": "Создать",
    }

    return render(request, "cashflow/reference_form.html", context)


def reference_update(request, reference_type, pk):
    config = get_reference_config(reference_type)
    model = config["model"]
    form_class = config["form"]

    instance = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, "Справочник успешно обновлён.")
            return redirect("cashflow:reference_list")
    else:
        form = form_class(instance=instance)

    context = {
        "form": form,
        "title": f"Редактировать {config['single_title']}",
        "button_text": "Сохранить",
    }

    return render(request, "cashflow/reference_form.html", context)


def reference_delete(request, reference_type, pk):
    config = get_reference_config(reference_type)
    model = config["model"]

    instance = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        try:
            instance.delete()
            messages.success(request, "Элемент справочника успешно удалён.")
        except ProtectedError:
            messages.error(
                request,
                "Нельзя удалить элемент справочника, потому что он уже используется в записях.",
            )

        return redirect("cashflow:reference_list")

    context = {
        "object": instance,
        "title": f"Удалить {config['single_title']}",
    }

    return render(request, "cashflow/reference_confirm_delete.html", context)