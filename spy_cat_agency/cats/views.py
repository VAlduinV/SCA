from django.shortcuts import render
from rest_framework import viewsets
from .models import Cat
from .serializers import CatSerializer

# Create your views here.


class CatViewSet(viewsets.ModelViewSet):
    """
        API ViewSet для управління моделлю Cat.

        Цей ViewSet надає стандартні дії для моделі Cat, такі як:
        - list: повертає список усіх котів.
        - retrieve: повертає дані про конкретного кота.
        - create: створює нового кота.
        - update: оновлює інформацію про кота.
        - partial_update: частково оновлює інформацію про кота.
        - destroy: видаляє кота.

        Атрибути:
            queryset (QuerySet): набір даних, що містить усіх котів.
            serializer_class (Serializer): серіалізатор для перетворення даних Cat у JSON і назад.
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
