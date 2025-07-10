from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.urls import reverse

from tasks.models import Task, TaskPermission

User = get_user_model()


class TaskListAPITestCase(APITestCase):
    """
    Тесты для проверки функциональности TaskListAPIView
    """

    def setUp(self) -> None:
        self.user1 = User.objects.create(login="user1")
        self.user1.set_password("1234")
        self.user1.save()
        self.user2 = User.objects.create(login="user2")
        self.user2.set_password("1234")
        self.user2.save()

        self.task1 = Task.objects.create(
            title="Погладить одежду",
            description="f f f",
            owner=self.user1
            # или author=self.user1, если у тебя поле называется иначе
        )

        self.task2 = Task.objects.create(
            title="Прибраться",
            owner=self.user2
        )

        refresh = RefreshToken.for_user(self.user1)
        access = refresh.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(access)}")

    def test_task_list(self) -> None:
        """
        Проверяет, что пользователь видит только свои задачи
        или задачи, к которым у него есть доступ.
        """
        url = reverse("tasks:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TaskPermissionCreateAPITestCase(APITestCase):
    """
    Тест на выдачу прав доступа к задаче.
    """

    def setUp(self) -> None:
        self.owner = User.objects.create(login="owner")
        self.owner.set_password("1234")
        self.owner.save()
        self.other = User.objects.create(login="other")
        self.other.set_password("1234")
        self.other.save()
        self.task = Task.objects.create(title="иымииыа", owner=self.owner)

        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

    def test_grant_read_permission(self) -> None:
        """
        Проверка, что владелец может выдать право на чтение.
        """
        url = reverse("tasks:permission_create")
        data = {
            "task": self.task.id,
            "user": self.other.id,
            "permission": "read"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TaskPermission.objects.filter(
            task=self.task,
            user=self.other,
            permission="read"
        ).exists())


class TaskPermissionDestroyAPITestCase(APITestCase):
    """
    Тест на отзыв прав доступа к задаче.
    """

    def setUp(self) -> None:
        self.owner = User.objects.create(login="owner")
        self.owner.set_password("1234")
        self.owner.save()
        self.reader = User.objects.create(login="reader")
        self.reader.set_password("1234")
        self.reader.save()
        self.task = Task.objects.create(title="Задача", owner=self.owner)

        self.permission = TaskPermission.objects.create(
            task=self.task, user=self.reader, permission="read"
        )

        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

    def test_revoke_permission(self) -> None:
        """
        Проверка, что владелец может отозвать права у пользователя.
        """
        url = reverse(
            "tasks:permission_delete",
            args=[self.permission.id]
        )
        self.assertTrue(TaskPermission.objects.filter(
            task=self.task,
            user=self.reader,
            permission="read"
        ).exists())
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TaskPermission.objects.filter(
            id=self.permission.id
        ).exists())


