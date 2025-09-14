from django.urls import path
from .views import StoryViewSet, LocalUploadView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"stories", StoryViewSet, basename="stories")
router.register(r"upload", LocalUploadView, basename="upload")  # updated

urlpatterns = router.urls
