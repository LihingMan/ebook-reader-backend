from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .serializers import RegistrationSerializer


# ================== Register User ===================#
class RegisterUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(
            data={"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
