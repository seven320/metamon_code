from django.contrib import admin

from .models import User, Task, Task_history

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Task_history)
class Task_historyAdmin(admin.ModelAdmin):
    pass