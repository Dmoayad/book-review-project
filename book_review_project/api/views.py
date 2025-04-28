# api/views.py

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Book, Review
from .serializers import (
    UserSerializer,
    BookSerializer,
    ReviewSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly


# --- Authentication Views ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        # Return the current authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Save the new password
            serializer.save()
            return Response(
                {"message": "Password updated successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Book Management Views ---
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, delete for Books.
    Create, Update, Delete restricted to Admin users.
    List and Retrieve available to anyone.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]


# --- Review Management Views ---
class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List all reviews for a specific book (GET).
    Create a new review for a specific book (POST).
    Requires authentication to create.
    """

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filter reviews based on the book_id in the URL
        book_id = self.kwargs['book_pk']
        get_object_or_404(Book, pk=book_id) # Ensure book exists
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        # Automatically set the user and book based on request context
        book_id = self.kwargs['book_pk']
        book = get_object_or_404(Book, pk=book_id)
        # Check if user already reviewed this book
        if Review.objects.filter(book=book, user=self.request.user).exists():
            raise ValidationError("You have already reviewed this book.")
        serializer.save(user=self.request.user, book=book)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, or Delete a specific review by its ID.
    Requires authentication.
    Only the owner of the review can update or delete it.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk' # Use 'pk' (the review ID) from the URL
