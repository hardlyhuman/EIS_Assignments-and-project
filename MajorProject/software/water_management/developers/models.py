from __future__ import unicode_literals

from django.db import models

# Create your models here.
from geoposition.fields import GeopositionField

class PointOfInterest(models.Model):
    name = models.CharField(max_length=100)
    position = GeopositionField()