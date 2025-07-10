from django.contrib import admin

from tasks.models import Task, TaskPermission


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id",]


@admin.register(TaskPermission)
class TaskPermissionAdmin(admin.ModelAdmin):
    list_display = ["id",]
