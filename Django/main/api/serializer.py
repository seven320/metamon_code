from rest_framework import serializers
from django_filters import rest_framework as filters

from .models import User, Task, Task_history

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'user_id', 'screen_name', 'created_at', 'secret_status')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task', 'user_id', 'created_at')

class Task_historySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_history
        fields = ('tweet_id', 'tweet_text', 'praised', 'task_id', 'created_at', 'user_id')

class SearchUserSerializer(filters.FilterSet):
    User_name = filters.CharFilter(field_name = 'user_id', lookup_expr = 'exact')

    class Meta:
        model = User
        fields = ('user_id',)

class SearchTaskSerializer(filters.FilterSet):
    Task_name = filters.CharFilter(lookup_expr = 'user_id')
    class Meta:
        model = Task
        fields = ('id', 'task', 'user_id', 'created_at')

class SearchTask_historySerializer(filters.FilterSet):
    Task_history_name = filters.CharFilter(lookup_expr = 'user_id')
    class Meta:
        model = Task_history
        fields = ('tweet_id', 'tweet_text', 'praised', 'task_id', 'created_at', 'user_id')