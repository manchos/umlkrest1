from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rd90.models import Rd90Calc
from rd90.serializers import Rd90CalcSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import permissions
# from django.contrib.auth.models import User
from profiles.models import CustomUser
from rd90.serializers import UserSerializer
from rest_framework import generics

# class Rd90CalcList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         rd90_calcs = Rd90Calc.objects.all()
#         serializer = Rd90CalcSerializer(rd90_calcs, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = Rd90CalcSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Rd90CalcList(generics.ListCreateAPIView):
    queryset = Rd90Calc.objects.all()
    serializer_class = Rd90CalcSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Rd90CalcDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rd90Calc.objects.all()
    serializer_class = Rd90CalcSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# class Rd90CalcDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Rd90Calc.objects.get(pk=pk)
#         except Rd90Calc.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         calc = self.get_object(pk)
#         serializer = Rd90CalcSerializer(calc)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         calc = self.get_object(pk)
#         serializer = Rd90CalcSerializer(calc, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         calc = self.get_object(pk)
#         calc.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
# @csrf_exempt
# def rd90_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         rd90_calcs = Rd90Calc.objects.all()
#         serializer = Rd90CalcSerializer(rd90_calcs, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = Rd90CalcSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def rd90_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         calc = Rd90Calc.objects.get(pk=pk)
#     except Rd90Calc.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = Rd90CalcSerializer(calc)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = Rd90CalcSerializer(calc, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         calc.delete()
#         return HttpResponse(status=204)