from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task, TaskPermission
from tasks.permissions import IsTaskOwnerFromObject, CanUpdateTask, CanReadTask, \
    IsTaskOwnerFromRequestData, IsTaskOwner
from tasks.serializers import TaskSerializer, TaskCreateSerializer, \
    TaskPermissionSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания новой задачи.
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: TaskCreateSerializer) -> None:
        serializer.save(owner=self.request.user)


class TaskListAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения списка задач,
    где пользователь — владелец или у него есть разрешение на чтение.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned_tasks = Task.objects.filter(owner=user)
        permitted_tasks = Task.objects.filter(
            permissions__user=user,
            permissions__permission="read"
        )
        return (owned_tasks | permitted_tasks).distinct()


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения одной задачи.
    Доступ разрешён владельцу или пользователю с правом чтения.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanReadTask]


class TaskUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления задачи.
    Доступ разрешён владельцу или пользователю с правом на изменение.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanUpdateTask]


class TaskDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления задачи.
    Доступ разрешён только владельцу задачи.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]


class TaskPermissionCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для выдачи прав на задачу определённому пользователю.
    Только владелец задачи может выдавать права.
    """
    permission_classes = [IsAuthenticated, IsTaskOwnerFromRequestData]
    queryset = TaskPermission.objects.all()
    serializer_class = TaskPermissionSerializer


class TaskPermissionDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для отзыва прав у пользователя.
    Доступ разрешён только владельцу задачи.
    """
    permission_classes = [IsAuthenticated, IsTaskOwnerFromObject]
    queryset = TaskPermission.objects.all()
    serializer_class = TaskPermissionSerializer
