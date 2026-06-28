from django import forms

from .models import (
    CashFlowRecord,
    Category,
    OperationType,
    Status,
    SubCategory,
)


class CashFlowRecordForm(forms.ModelForm):
    """
    Cash flow record creation/editing form.
    """

    class Meta:
        model = CashFlowRecord

        fields = [
            "created_at",
            "status",
            "operation_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]

        widgets = {
            "created_at": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "operation_type": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_operation_type",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_category",
                }
            ),
            "subcategory": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_subcategory",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "1000.00",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Комментарий необязателен",
                }
            ),
        }

        labels = {
            "created_at": "Дата",
            "status": "Статус",
            "operation_type": "Тип операции",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "amount": "Сумма",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.none()
        self.fields["subcategory"].queryset = SubCategory.objects.none()

        if self.data:
            operation_type_id = self.data.get("operation_type")
            category_id = self.data.get("category")

            if operation_type_id:
                self.fields["category"].queryset = Category.objects.filter(operation_type_id=operation_type_id)

            if category_id:
                self.fields["subcategory"].queryset = SubCategory.objects.filter(category_id=category_id)

        elif self.instance and self.instance.pk:
            self.fields["category"].queryset = Category.objects.filter(
                operation_type=self.instance.operation_type
            )
            self.fields["subcategory"].queryset = SubCategory.objects.filter(
                category=self.instance.category
            )

    def clean(self):
        """
        Server-side form validation.
        """

        cleaned_data = super().clean()

        operation_type = cleaned_data.get("operation_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if operation_type and category:
            if category.operation_type_id != operation_type.id:
                self.add_error(
                    "category",
                    "Категория не относится к выбранному типу операции.",
                )

        if category and subcategory:
            if subcategory.category_id != category.id:
                self.add_error(
                    "subcategory",
                    "Подкатегория не относится к выбранной категории.",
                )

        return cleaned_data


class CashFlowRecordFilterForm(forms.Form):
    """
    Record filtering form on the main page.
    """

    date_from = forms.DateField(
        required=False,
        label="Дата от",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    date_to = forms.DateField(
        required=False,
        label="Дата до",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    status = forms.ModelChoiceField(
        required=False,
        label="Статус",
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    operation_type = forms.ModelChoiceField(
        required=False,
        label="Тип операции",
        queryset=OperationType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    category = forms.ModelChoiceField(
        required=False,
        label="Категория",
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    subcategory = forms.ModelChoiceField(
        required=False,
        label="Подкатегория",
        queryset=SubCategory.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Бизнес",
                }
            )
        }
        labels = {
            "name": "Название",
        }


class OperationTypeForm(forms.ModelForm):
    class Meta:
        model = OperationType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Списание",
                }
            )
        }
        labels = {
            "name": "Название",
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "operation_type"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Маркетинг",
                }
            ),
            "operation_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        labels = {
            "name": "Название",
            "operation_type": "Тип операции",
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Avito",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        labels = {
            "name": "Название",
            "category": "Категория",
        }