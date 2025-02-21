from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Loan, Reservation, Review, CustomUser, Profile
from django.contrib.auth import get_user_model

class BookSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "category", "is_available", "added_by", "created_at"]
        read_only_fields = ["id", "added_by", "created_at"]

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")  # Dodajemy role

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            role=validated_data.get("role", "reader"),  # Domyślnie czytelnik
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class LoanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    due_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")
    fine = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "book", "book_title", "user", "user_username", "loan_date", "due_date", "returned_at", "status", "fine"]
        read_only_fields = ["id", "loan_date", "returned_at", "status", "user", "fine"]

    def validate(self, data):
        book = data.get("book")
        if book and not book.is_available:
            raise serializers.ValidationError("Book is currently unavailable.")
        return data
    

class ReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Reservation
        fields = ["id", "book", "book_title", "user", "user_username", "created_at", "expires_at", "status"]
        read_only_fields = ["id", "created_at", "expires_at", "status", "user"]
    
    def validate(self, data):
        book = data.get("book")
        if book and not book.is_available:
            raise serializers.ValidationError("Book is currently unavailable.")
        return data
    

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Review
        fields = ["id", "book", "user", "user_username", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Profile
        fields = ["id", "user", "user_username", "phone_number", "address", "activity_history"]
        read_only_fields = ["id", "user", "user_username"]
