# lazymenu/lazymenu/urls.py : Main urls.py
from django.contrib import admin
from django.urls import path, include
from lazymenu_api import urls as lazymenu_urls

urlpatterns = [
    path('todos/', include(lazymenu_urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]