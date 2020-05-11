from django.contrib.auth.models import AbstractUser
from django.db import models
from novelas.models import Novelas,allchaps


class CustomUser(AbstractUser):
    favoritos = models.ManyToManyField(Novelas)
    historial = models.ManyToManyField(allchaps)
    linkdonaciones = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.username

# Create your models here.
