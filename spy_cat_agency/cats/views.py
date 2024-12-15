from django.shortcuts import render
from rest_framework import viewsets
from .models import Cat
from .serializers import CatSerializer

# Create your views here.


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
