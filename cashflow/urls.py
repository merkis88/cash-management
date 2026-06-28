from django.urls import path

from . import views

app_name = "cashflow"

urlpatterns = [
    path("", views.record_list, name="record_list"),
    path("records/create/", views.record_create, name="record_create"),
    path("records/<int:pk>/edit/", views.record_update, name="record_update"),
    path("records/<int:pk>/delete/", views.record_delete, name="record_delete"),
    path("api/categories/", views.categories_by_operation_type, name="categories_by_operation_type"),
    path("api/subcategories/", views.subcategories_by_category, name="subcategories_by_category"),
    path("references/", views.reference_list, name="reference_list"),
    path("references/<str:reference_type>/create/", views.reference_create, name="reference_create"),
    path("references/<str:reference_type>/<int:pk>/edit/", views.reference_update, name="reference_update"),
    path("references/<str:reference_type>/<int:pk>/delete/", views.reference_delete, name="reference_delete"),
]