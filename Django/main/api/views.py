from django.shortcuts import render

from rest_framework import viewsets, filters

from .models import User, Task, Task_history
from .serializer import UserSerializer, TaskSerializer, Task_historySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    class Meta:
        lookup_field = "user_id"

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    class Meta:
        lookup_field = "task_id"

class Task_historyViewSet(viewsets.ModelViewSet):
    queryset = Task_history.objects.all()
    serializer_class = Task_historySerializer

    # class Meta:
    #     lookup_field = "task_"
