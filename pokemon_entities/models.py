from django.db import models
import math


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="pokemons", null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"{round(lat, 3)}: {round(lon, 3)}"
