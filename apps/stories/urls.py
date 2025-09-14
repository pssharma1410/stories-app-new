from django.urls import path
from rest_framework import routers
from .views import StoryViewSet, LocalUploadView

router = routers.DefaultRouter()
router.register(r"stories", StoryViewSet, basename="stories")
router.register(r"upload", LocalUploadView, basename="upload")

urlpatterns = router.urls
