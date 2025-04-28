from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    ChangePasswordView,
    BookViewSet,
    ReviewListCreateView,
    ReviewDetailView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
# The 'basename' is important if queryset is overridden or not set

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ), # POST: Obtain JWT
    path(
        'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ), # POST: Refresh JWT
    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name='change_password',
    ), # POST: Change password
    # Book Management (uses router)
    path('', include(router.urls)),
    # Review Management
    path(
        'books/<int:book_pk>/reviews/',
        ReviewListCreateView.as_view(),
        name='review-list-create',
    ), # GET: List reviews, POST: Create review
    path(
        'reviews/<int:pk>/',
        ReviewDetailView.as_view(),
        name='review-detail',
    ), # GET/PUT/DELETE specific review
]
