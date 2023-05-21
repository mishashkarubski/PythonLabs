from django.urls import path

from workshop.views import index

urlpatterns = [
    path('', index),
]
