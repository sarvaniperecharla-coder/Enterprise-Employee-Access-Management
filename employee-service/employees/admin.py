from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "designation",
        "salary",
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "designation",
        "is_active",
    )

    ordering = ("first_name",)