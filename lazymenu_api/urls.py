# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from .views import (
    LazyMenuListApiView,
)

urlpatterns = [
    path('api', LazyMenuListApiView.as_view()),
]

#SUPER USER
# arturobravorovirosa
