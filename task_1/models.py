from django.db import models
from django.utils import timezone


class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    points = models.IntegerField(default=0)
    first_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.first_login:
            self.first_login = timezone.now()
        super().save(*args, **kwargs)

    def add_points(self, points):
        self.points += points
        self.save()

    def add_boost(self, name, description='', manually_awarded=False):
        Boost.objects.create(
            player=self,
            name=name,
            description=description,
            manually_awarded=manually_awarded
        )

    def __str__(self):
        return self.username


class Boost(models.Model):
    player = models.ForeignKey(Player, related_name='boosts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    obtained_at = models.DateTimeField(default=timezone.now)
    manually_awarded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'name')

    def __str__(self):
        return f'{self.player.username} - {self.name}'
