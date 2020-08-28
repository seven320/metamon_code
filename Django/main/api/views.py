from django.shortcuts import render

from rest_framework import viewsets, filters

from .models import User, Task, Task_history
from .serializer import UserSerializer, TaskSerializer, Task_historySerializer
from .serializer import SearchUserSerializer, SearchTaskSerializer, SearchTask_historySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    class META:
        lookup_field = 'user_id'

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    class META:
        lookup_field = 'task_id'

class Task_historyViewSet(viewsets.ModelViewSet):
    queryset = Task_history.objects.all()
    serializer_class = Task_historySerializer

# 検索
class SearchUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = SearchUserSerializer
    filterset_fields = ['user_id']

class SearchTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = SearchTaskSerializer

class SearchTask_historyViewSet(viewsets.ModelViewSet):
    queryset = Task_history.objects.all()
    serializer_class = Task_historySerializer
    filter_class = SearchTask_historySerializer


