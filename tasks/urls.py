from rest_framework.urls import path
from tasks.apps import TasksConfig

from tasks.views import (
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDestroyAPIView,
    TaskCreateAPIView,
    # GrantPermissionView,
    # RevokePermissionView
    TaskPermissionCreateAPIView,
    TaskPermissionDestroyAPIView
)

app_name = TasksConfig.name

urlpatterns = [
    path("create/", TaskCreateAPIView.as_view(), name="create"),
    path("list/", TaskListAPIView.as_view(), name="list"),
    path("detail/<int:pk>/", TaskRetrieveAPIView.as_view(), name="detail"),
    path("update/<int:pk>/", TaskUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", TaskDestroyAPIView.as_view(), name="delete"),
    # path(
    #     "permissions/grant/",
    #     GrantPermissionView.as_view(),
    #     name="grant_permission"
    # ),
    # path(
    #     "permissions/revoke/",
    #     RevokePermissionView.as_view(),
    #     name="revoke_permission"
    # ),
    path(
        "permissions/create/",
        TaskPermissionCreateAPIView.as_view(),
        name="permission_create"
    ),
    path(
        "permissions/delete/<int:pk>/",
        TaskPermissionDestroyAPIView.as_view(),
        name="permission_delete"
    ),
]
