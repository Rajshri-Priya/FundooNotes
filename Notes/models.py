from django.db import models
from user_auth.models import CustomUser


# Create your models here.
class Labels(models.Model):
    """
     Labels Model : name, user_id, created_at, modified_at
    """
    name = models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    """
            Notes Model : title, description, user_id, created_at, modified_at, collaborator, label...
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(CustomUser, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='notes_images/', null=True, blank=True)
    # image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Note"
