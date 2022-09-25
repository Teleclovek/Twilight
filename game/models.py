from cProfile import label
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings


class Game(models.Model):
    gamename = models.CharField(max_length=25, verbose_name='Jméno hry')
    gamesize = models.IntegerField( verbose_name='Počet hráčů',
        validators=[MaxValueValidator(6),MinValueValidator(1)])
    pok = models.BooleanField(default=True)
    codex = models.BooleanField(default=True)
    picking = models.IntegerField(default=1)

    def __str__(self):
        return self.gamename

class RaceDefault(models.Model):
    racename = models.CharField(max_length=25)
    default = models.BooleanField(default=True)
    pok = models.BooleanField(default=False)
    codex = models.BooleanField(default=False)

    def __str__(self):
        return self.racename

class Race(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)
    racename = models.CharField(max_length=25)
    pok = models.BooleanField(default=False)
    codex = models.BooleanField(default=False)
    racegameorder = models.IntegerField()
    in_game = models.BooleanField(default=False)
    voted = models.BooleanField(default=False)
    chosen = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    taken = models.BooleanField(default=False)

    def __str__(self):
        return self.racename

class Mapposition(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)
    position = models.IntegerField(null = True, blank=True)
    taken = models.BooleanField(default=False)

    def __str__(self):
        return 'Pozice č.{}'.format(self.position)


class Player(models.Model):
    playername = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)
    gameorder = models.IntegerField(
        validators=[MaxValueValidator(6),MinValueValidator(1)])
    speaker = models.BooleanField(default=False)
    mappositon = models.ForeignKey(Mapposition, on_delete=models.CASCADE,null = True, blank=True)
    chosenrace = models.ForeignKey(Race, on_delete=models.CASCADE, null = True, blank=True)
    voted = models.BooleanField(default=False)
    drafted = models.BooleanField(default=False)

    def __str__(self):
        return self.playername.username
