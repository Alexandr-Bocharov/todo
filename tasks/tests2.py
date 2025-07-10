# class TaskPermissionCreateAPITestCase(APITestCase):
#     def setUp(self):
#         self.owner = User.objects.create(login="owner")
#         self.owner.set_password("1234")
#         self.owner.save()
#         self.other = User.objects.create(login="other")
#         self.other.set_password("1234")
#         self.other.save()
#         self.task = Task.objects.create(title="иымииыа", owner=self.owner)
#
#         refresh = RefreshToken.for_user(self.owner)
#         self.client.credentials(
#             HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
#         )
#
#     def test_grant_read_permission(self):
#         url = reverse("tasks:permission_create")
#         data = {
#             "task": self.task.id,
#             "user": self.other.id,
#             "permission": "read"
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(TaskPermission.objects.filter(
#             task=self.task,
#             user=self.other,
#             permission="read"
#         ).exists())
#
#
# class TaskPermissionDestroyAPITestCase(APITestCase):
#     def setUp(self):
#         self.owner = User.objects.create(login="owner")
#         self.owner.set_password("1234")
#         self.owner.save()
#         self.reader = User.objects.create(login="reader")
#         self.reader.set_password("1234")
#         self.reader.save()
#         self.task = Task.objects.create(title="Задача", owner=self.owner)
#
#         self.permission = TaskPermission.objects.create(
#             task=self.task, user=self.reader, permission="read"
#         )
#
#         refresh = RefreshToken.for_user(self.owner)
#         self.client.credentials(
#             HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
#         )
#
#     def test_revoke_permission(self):
#         url = reverse(
#             "tasks:permission_delete",
#             args=[self.permission.id]
#         )
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(TaskPermission.objects.filter(
#             id=self.permission.id
#         ).exists())