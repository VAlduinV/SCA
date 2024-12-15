from django.db import models
from cats.models import Cat

# Create your models here.

class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id} - Completed: {self.is_completed}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Target {self.name} ({self.country})"
