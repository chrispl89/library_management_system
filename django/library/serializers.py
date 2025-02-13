from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    # Używamy StringRelatedField, aby uniknąć problemów rekurencyjnych
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "category", "added_by", "created_at"]
        read_only_fields = ["id", "added_by", "created_at"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
