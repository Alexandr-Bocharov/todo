from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .models import Task, TaskPermission


class IsTaskOwnerFromRequestData(BasePermission):
    """
    Проверяет, что request.user — владелец задачи, указанной в теле запроса.
    Используется в CreateAPIView, где объект ещё не существует.
    """
    def has_permission(self, request, view):
        task_id = request.data.get('task')
        if not task_id:
            return False
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return False
        return task.owner == request.user


class IsTaskOwnerFromObject(BasePermission):
    """
    Проверяет, что request.user является владельцем задачи,
    через объект TaskPermission.
    """
    def has_object_permission(
            self, request: Request, view, obj: TaskPermission
    ) -> bool:
        return obj.task.owner == request.user


class IsTaskOwner(BasePermission):
    """
    Проверяет, что request.user является владельцем задачи.
    """
    def has_object_permission(self, request: Request, view, obj: Task) -> bool:
        return obj.owner == request.user


class CanUpdateTask(BasePermission):
    """
    Проверяет, имеет ли пользователь право обновлять задачу.
    """
    def has_object_permission(self, request: Request, view, obj: Task) -> bool:
        if obj.owner == request.user:
            return True
        return TaskPermission.objects.filter(
            task=obj,
            user=request.user,
            permission="update"
        ).exists()


class CanReadTask(BasePermission):
    """
    Проверяет, имеет ли пользователь право читать задачу.
    """

    def has_object_permission(self, request: Request, view, obj: Task) -> bool:
        if obj.owner == request.user:
            return True
        return TaskPermission.objects.filter(
            task=obj,
            user=request.user,
            permission="read"
        ).exists()