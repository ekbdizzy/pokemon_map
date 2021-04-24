from django.db import models
import math


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="pokemons", null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="pokemon")
    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pokemon.title}: {round(self.lat, 3)}: {round(self.lon, 3)}"
