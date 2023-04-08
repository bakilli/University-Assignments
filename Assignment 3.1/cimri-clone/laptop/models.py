from django.db import models

# Create your models here.

class Laptop(models.Model):
    name = models.CharField(max_length=200, blank= True, null = True)
    brand = models.CharField(max_length=50, blank= True, null = True)
    model = models.TextField(blank= True, null = True)
    operating_system = models.CharField(max_length=50, blank= True, null = True)
    cpu = models.CharField(max_length=50, blank= True, null = True)
    gpu = models.CharField(max_length=50, blank= True, null = True)
    ram = models.IntegerField(blank= True, null = True)
    disc = models.IntegerField(blank= True, null = True)
    disc_type = models.CharField(max_length=50, blank= True, null = True)
    screen_size = models.FloatField(blank= True, null = True)
    rating = models.FloatField(blank= True, null = True)
    price = models.FloatField(blank= True, null = True)
    site = models.CharField(max_length=50, blank= True, null = True)
    site_link = models.URLField(blank= True, null = True)
    

    def __str__(self):
        return self.name