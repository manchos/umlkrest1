from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rd90.models import Rd90Calc
from api.serializers import Rd90CalcSerializer


class Rd90ListView(generics.ListAPIView):
    queryset = Rd90Calc.objects.all()
    serializer_class = Rd90CalcSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Rd90Calc.objects.all()
    serializer_class = Rd90CalcSerializer