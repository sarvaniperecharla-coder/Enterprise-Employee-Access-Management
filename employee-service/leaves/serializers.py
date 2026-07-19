from rest_framework import serializers
from .models import LeaveType, Leave
from datetime import timedelta


class LeaveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType
        fields = "__all__"



class LeaveSerializer(serializers.ModelSerializer):

    duration = serializers.SerializerMethodField()


    class Meta:
        model = Leave
        fields = [
            "id",
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "created_at",
            "duration"
        ]


    def get_duration(self, obj):

        return (
            obj.end_date - obj.start_date
        ).days + 1



    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")
        employee = data.get("employee")
        leave_type = data.get("leave_type")


        # Check date validity

        if end_date < start_date:

            raise serializers.ValidationError(
                {
                    "end_date":
                    "End date cannot be before start date"
                }
            )


        requested_days = (
            end_date - start_date
        ).days + 1



        # Calculate already used leave

        approved_leaves = Leave.objects.filter(
            employee=employee,
            leave_type=leave_type,
            status="Approved"
        )


        used_days = 0


        for leave in approved_leaves:

            used_days += (
                leave.end_date - leave.start_date
            ).days + 1



        remaining_days = (
            leave_type.max_days - used_days
        )


        if requested_days > remaining_days:

            raise serializers.ValidationError(
                {
                    "leave":
                    f"Insufficient balance. Remaining days: {remaining_days}"
                }
            )


        return data