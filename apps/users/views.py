from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User, Follow
from apps.users.serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        target = self.get_object()
        if request.user.id == target.id:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, followee=target)
        if created:
            return Response({"detail": f"You are now following {target.username}."}, status=201)
        return Response({"detail": f"You already follow {target.username}."}, status=200)

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        deleted, _ = Follow.objects.filter(follower=request.user, followee=target).delete()
        if deleted:
            return Response({"detail": f"You have unfollowed {target.username}."}, status=200)
        return Response({"detail": f"You were not following {target.username}."}, status=400)



User = get_user_model()


class LoginOrSignupView(APIView):
    permission_classes = [AllowAny]  # AllowAny

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", f"{username}@example.com")

        if not username or not password:
            return Response({"detail": "username and password required"}, status=400)

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"detail": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=200)
