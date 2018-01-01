from django.db import models
from django.conf import settings
from django.core.files import File

# Create your models here.
class Image(models.Model):
    imageFile = models.ImageField(upload_to = "./")
    imageName = models.TextField(default="")
    uploaded_at = models.DateTimeField(auto_now_add = True)

class Histogram(models.Model):
    image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        blank=True,
        related_name = "histogram"
    )
    imageHist = models.ImageField()
    histName = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add = True)

class EqualizedHistogram(models.Model):
    histogram = models.OneToOneField(
        Histogram,
        on_delete=models.CASCADE,
        related_name = "equalized"
    )
    eqHist = models.ImageField()
    eqName = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add = True)

class EqualizedImage(models.Model):
    image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        related_name = "equalized_image"
    )
    eqImage = models.ImageField(upload_to = "./")
    eqImageName = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add = True)
