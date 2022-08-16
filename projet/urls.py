from django.urls import path
from . import views
urlpatterns = [
    path('cree_projet', views.cree_projet, name='cree_projet'),
]
