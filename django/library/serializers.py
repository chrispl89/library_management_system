from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Loan

class BookSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "category", "is_available", "added_by", "created_at"]
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

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Loan
        fields = ["id", "book", "book_title", "user", "user_username", "loan_date", "due_date", "returned_at", "status"]
        read_only_fields = ["id", "loan_date", "returned_at", "status"]

    def validate(self, data):
        book = data.get("book")
        if book and not book.is_available:
            raise serializers.ValidationError("Book is already borrowed!")
        return data