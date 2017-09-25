from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='photo/')
    modified_image = models.ImageField(
        upload_to='photo/',
        null=True,
        blank=True
    )


class VisionFaceDetails(models.Model):
    anger = models.CharField(max_length=50)
    joy = models.CharField(max_length=50)
    surprise = models.CharField(max_length=50)
    sorrow = models.CharField(max_length=50)
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="face_detail"
    )


class VisionLabelsDetails(models.Model):
    labels = models.CharField(max_length=100)
    score = models.FloatField()
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="label_detail"
    )
