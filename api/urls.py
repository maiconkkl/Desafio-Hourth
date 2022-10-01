from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('teste_tecnico', views.Api.as_view()),
]
