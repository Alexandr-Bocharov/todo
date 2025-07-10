from django.db import models
from django.contrib.auth import get_user_model

from utils import NULLABLE

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    created_at = models.DateTimeField(
        verbose_name="дата создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="дата обновления", auto_now=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="создатель",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title


class TaskPermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('update', 'Update'),
    ]

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='permissions'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='task_permissions'
    )
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('task', 'user', 'permission')

    def __str__(self):
        return (f"Право на {self.permission} на задачу {self.task} "
                f"для {self.user}")
