from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from leaves.models import Leave, LeaveType
from employees.permissions import IsManager
from notifications.models import Notification
from employees.models import Employee


class EmployeeDashboardView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        employee = request.user.employee_profile

        leaves = Leave.objects.filter(
            employee=employee
        )


        summary = {
            "total_applied": leaves.count(),

            "approved": leaves.filter(
                status="Approved"
            ).count(),

            "pending": leaves.filter(
                status="Pending"
            ).count(),

            "rejected": leaves.filter(
                status="Rejected"
            ).count(),
        }


        balances = []

        for leave_type in LeaveType.objects.all():

            approved_leaves = leaves.filter(
                leave_type=leave_type,
                status="Approved"
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
                        0
                    )
                }
            )


        notifications = Notification.objects.filter(
            user=request.user
        )


        return Response(
            {

                "employee": {

                    "name": str(employee),

                    "email": employee.email,

                    "department": (
                        employee.department.name
                        if employee.department
                        else None
                    ),

                    "designation": employee.designation,

                    "date_of_joining": employee.date_of_joining
                },


                "leave_summary": summary,


                "leave_balance": balances,


                "notifications": {

                    "total": notifications.count(),

                    "unread": notifications.filter(
                        is_read=False
                    ).count()
                }

            }
        )





class ManagerDashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]


    def get(self, request):

        manager = request.user.employee_profile


        department = manager.department


        team_members = Employee.objects.filter(
            department=department
        )


        team_leaves = Leave.objects.filter(
            employee__department=department
        )


        return Response(
            {

                "manager": {

                    "name": str(manager),

                    "department": (
                        department.name
                        if department
                        else None
                    )

                },


                "team_information": {

                    "team_size": team_members.count()

                },


                "leave_summary": {

                    "total_requests": team_leaves.count(),

                    "pending": team_leaves.filter(
                        status="Pending"
                    ).count(),

                    "approved": team_leaves.filter(
                        status="Approved"
                    ).count(),

                    "rejected": team_leaves.filter(
                        status="Rejected"
                    ).count(),

                }

            }
        )