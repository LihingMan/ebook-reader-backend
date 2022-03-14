from django.http import JsonResponse
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
