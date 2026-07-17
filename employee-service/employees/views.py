from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Employee
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Search functionality
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "designation",
    ]

    # Filter functionality
    filterset_fields = [
        "designation",
        "is_active",
    ]

    # Ordering functionality
    ordering_fields = [
        "salary",
        "date_of_joining",
        "first_name",
    ]

    # Default ordering
    ordering = ["first_name"]