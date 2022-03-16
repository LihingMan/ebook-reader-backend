from django.http import JsonResponse
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from modules.ebook.models import Ebooks
from .core_serializers import EbookSerializer

from rest_framework import serializers


class UploadEbookView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EbookSerializer


class RetrieveListEbookViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    serializer_class = EbookSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        ebook_id = self.request.query_params.get("ebook_id")

        if not user_id:
            raise serializers.ValidationError({"msg": "Please specify a user"})

        queryset = Ebooks.objects.filter(user=user_id)

        if ebook_id:
            queryset = queryset.filter(id=ebook_id)

        return queryset.order_by("title")
