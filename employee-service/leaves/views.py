from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from employees.permissions import IsManager
from notifications.models import Notification

from .models import LeaveType, Leave
from .serializers import LeaveTypeSerializer, LeaveSerializer


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    search_fields = ["name"]
    ordering_fields = ["name", "max_days"]
    ordering = ["name"]


class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = [
        "employee",
        "leave_type",
        "status",
    ]

    search_fields = [
        "reason",
        "status",
    ]

    ordering_fields = [
        "start_date",
        "end_date",
        "status",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "employee_profile"):
            return Leave.objects.none()

        employee = user.employee_profile

        # HR can see all leaves
        if employee.role == "HR":
            return Leave.objects.all()

        # Manager can see department leaves
        if employee.role == "Manager":
            return Leave.objects.filter(
                employee__department=employee.department
            )

        # Employee can see only their own leaves
        return Leave.objects.filter(
            employee=employee
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="approve",
        permission_classes=[IsManager],
    )
    def approve_leave(self, request, pk=None):

        leave = self.get_object()

        if leave.status != "Pending":
            return Response(
                {
                    "error": "Only pending leaves can be approved"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave.status = "Approved"
        leave.save()

        if leave.employee.user:
            Notification.objects.create(
                user=leave.employee.user,
                message=f"Your {leave.leave_type.name} request has been approved."
            )

        return Response(
            {
                "message": "Leave approved successfully",
                "leave_id": leave.id,
                "status": leave.status,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="reject",
        permission_classes=[IsManager],
    )
    def reject_leave(self, request, pk=None):

        leave = self.get_object()

        if leave.status != "Pending":
            return Response(
                {
                    "error": "Only pending leaves can be rejected"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave.status = "Rejected"
        leave.save()

        if leave.employee.user:
            Notification.objects.create(
                user=leave.employee.user,
                message=f"Your {leave.leave_type.name} request has been rejected."
            )

        return Response(
            {
                "message": "Leave rejected successfully",
                "leave_id": leave.id,
                "status": leave.status,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="employee",
                description="Employee ID",
                required=True,
                type=int,
            )
        ]
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="balance",
    )
    def leave_balance(self, request):

        employee_id = request.query_params.get("employee")

        if not employee_id:
            return Response(
                {
                    "error": "Employee id is required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave_types = LeaveType.objects.all()
        balances = []

        for leave_type in leave_types:

            approved_leaves = Leave.objects.filter(
                employee_id=employee_id,
                leave_type=leave_type,
                status="Approved",
            )

            used_days = 0

            for leave in approved_leaves:
                used_days += (
                    leave.end_date - leave.start_date
                ).days + 1

            balances.append(
                {
                    "leave_type": leave_type.name,
                    "allowed_days": leave_type.max_days,
                    "used_days": used_days,
                    "remaining_days": max(
                        leave_type.max_days - used_days,
                        0,
                    ),
                }
            )

        return Response(
            {
                "employee": employee_id,
                "leave_balances": balances,
            },
            status=status.HTTP_200_OK,
        )