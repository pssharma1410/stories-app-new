from django.urls import path, include
from rest_framework import routers
from apps.users.views import UserViewSet, LoginOrSignupView
from rest_framework_simplejwt.views import TokenRefreshView

# Register UserViewSet without repeating "users"
router = routers.DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    # More specific paths should come first
    path("auth/", LoginOrSignupView.as_view(), name="login_or_signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # The general router path comes last
    path("", include(router.urls)),
]