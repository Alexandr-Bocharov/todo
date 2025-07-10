from rest_framework import serializers
from django.contrib.auth import get_user_model

from tasks.models import Task, TaskPermission

User = get_user_model()


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания задачи.
    """
    class Meta:
        model = Task
        fields = ("title",)


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения задачи.
    """
    class Meta:
        model = Task
        fields = "__all__"


class TaskPermissionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели прав доступа к задаче.
    """
    class Meta:
        model = TaskPermission
        fields = ["id", "task", 'user', 'permission']



