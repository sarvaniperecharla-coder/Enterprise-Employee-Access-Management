from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    filterset_fields = [
        "department",
        "role",
        "is_active",
    ]


    search_fields = [
        "first_name",
        "last_name",
        "email",
        "designation",
    ]


    ordering_fields = [
        "first_name",
        "salary",
        "date_of_joining",
    ]


    ordering = [
        "first_name"
    ]