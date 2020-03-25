from django.db import models

# Create your models here.

class Pose_model(models.Model):
    pose_array = models.TextField(blank=True, null=True)
