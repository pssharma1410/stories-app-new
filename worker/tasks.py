from celery import shared_task
from django.utils import timezone
from apps.stories.models import Story
import logging

logger = logging.getLogger(__name__)


@shared_task
def expire_stories():
    now = timezone.now()
    qs = Story.objects.filter(expires_at__lt=now, deleted_at__isnull=True)
    count = qs.count()
    qs.update(deleted_at=now)
    logger.info({"event": "story_expired", "count": count})
    return count
