from django.db import models

class Player(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name