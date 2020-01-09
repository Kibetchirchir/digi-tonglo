from django.db import models

class UtilityList(models.Model):
    name = models.CharField(max_length=225)
    service = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    
