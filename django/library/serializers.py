from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Loan, Reservation, Review, CustomUser, Profile
from django.contrib.auth import get_user_model


class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model data for API operations"""
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Metadata defining exposed fields and read-only properties"""
        model = Book
        fields = ["id", "title", "author", "category", "is_available", "added_by", "created_at"]
        read_only_fields = ["id", "added_by", "created_at"]

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Handles user registration with password hashing and role assignment"""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        """Configuration for registration fields"""
        model = User
        fields = ("id", "username", "email", "password", "role")

    def create(self, validated_data):
        """Creates new user with hashed password and default role"""
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            role=validated_data.get("role", "reader"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoanSerializer(serializers.ModelSerializer):
    """Serializes loan operations with automatic user association"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    due_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")
    fine = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        """Loan representation configuration"""
        model = Loan
        fields = ["id", "book", "book_title", "user", "user_username", "loan_date", "due_date", "returned_at", "status", "fine"]
        read_only_fields = ["id", "loan_date", "returned_at", "status", "user", "fine"]

    def validate(self, data):
        """Ensures book availability before creating loan"""
        book = data.get("book")
        if book and not book.is_available:
            raise serializers.ValidationError("Book is currently unavailable.")
        return data


class ReservationSerializer(serializers.ModelSerializer):
    """Handles book reservation operations"""
    book_title = serializers.ReadOnlyField(source="book.title")
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        """Reservation data structure configuration"""
        model = Reservation
        fields = ["id", "book", "book_title", "user", "user_username", "created_at", "expires_at", "status"]
        read_only_fields = ["id", "created_at", "expires_at", "status", "user"]
    
    def validate(self, data):
        """Validates book availability for reservation"""
        book = data.get("book")
        if book and not book.is_available:
            raise serializers.ValidationError("Book is currently unavailable.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes book reviews and ratings"""
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        """Review data exposure configuration"""
        model = Review
        fields = ["id", "book", "user", "user_username", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    """Manages user profile data with access control"""
    user_username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        """Profile field configuration"""
        model = Profile
        fields = ["id", "user", "user_username", "phone_number", "address", "activity_history"]
        read_only_fields = ["id", "user", "user_username", "activity_history"]

    def update(self, instance, validated_data):
        """Ensures users can only update their own profile"""
        user = self.context["request"].user
        if instance.user != user:
            raise serializers.ValidationError("You can only edit your own profile.")
        return super().update(instance, validated_data)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializes basic user information for display"""
    class Meta:
        """User data exposure configuration"""
        model = User
        fields = ["id", "username", "email", "role"]
