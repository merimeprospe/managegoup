from django.urls import path
from . import views
urlpatterns = [
    path('invitation', views.invitation),
]
