import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.common.managers import IsDeletedManager, GetOrNoneManager


class BaseModel(models.Model):
    """
    A base model class that includes common fields and methods for all models.

    Attributes:
        id (UUIDField): Unique identifier for the model instance.
        created_at (DateTimeField): Timestamp when the instance was created.
        updated_at (DateTimeField): Timestamp when the instance was last updated.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True



class IsDeletedModel(BaseModel):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = IsDeletedManager()

    def delete(self, *args, **kwargs):
        # Мягкое удаление is_deleted=True
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Content(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Автор")
    metadata = models.JSONField(default=dict, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Article(Content):
    text = models.TextField()
    word_count = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        text = self.text
        self.word_count = len(text.split())
        super().save(*args, **kwargs)



class Video(Content):
    video_url = models.URLField()
    duration = models.DurationField(null=True, blank=True)

class Image(Content):
    image = models.ImageField(upload_to="images/")
    dimensions = models.CharField(max_length=255, blank=True, null=True)




