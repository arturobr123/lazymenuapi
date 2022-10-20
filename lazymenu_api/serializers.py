# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Todo
class LazyMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]