from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    photo = models.FileField(upload_to='photo/')
