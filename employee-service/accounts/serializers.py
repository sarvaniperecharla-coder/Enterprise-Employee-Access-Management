from rest_framework import serializers
from django.contrib.auth.models import User

from employees.models import Employee


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    employee_id = serializers.IntegerField(
        write_only=True
    )


    def create(self, validated_data):

        employee_id = validated_data.pop("employee_id")

        try:
            employee = Employee.objects.get(
                id=employee_id
            )

        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "employee_id": "Employee not found."
                }
            )

        if employee.user:
            raise serializers.ValidationError(
                {
                    "employee_id": "This employee already has a user account."
                }
            )

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        employee.user = user
        employee.save()

        return user


    def to_representation(self, instance):

        return {
            "message": "User registered successfully.",
            "username": instance.username,
            "employee_id": instance.employee_profile.id
        }