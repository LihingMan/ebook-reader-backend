from rest_framework import serializers
from .models import User, Ebooks
from utils.choices import Role


class EbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebooks
        exclude = ["created_at"]
