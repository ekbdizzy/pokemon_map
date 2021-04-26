from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название (анг.)")
    title_jp = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название (яп.)")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name='previous',
                                           verbose_name="Из кого эволюционировал")
    image = models.ImageField(upload_to="pokemons", null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities", verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")

    appeared_at = models.DateTimeField(verbose_name="Когда появится")
    disappeared_at = models.DateTimeField(verbose_name="Когда исчезнет")

    level = models.IntegerField(default=0, verbose_name="Уровень")
    health = models.IntegerField(default=0, verbose_name="Здоровье")
    strength = models.IntegerField(default=0, verbose_name="Атака")
    defence = models.IntegerField(default=0, verbose_name="Защита")
    stamina = models.IntegerField(default=0, verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title_ru} ур. {self.level} | {round(self.lat, 3)}: {round(self.lon, 3)}"

    class Meta:
        verbose_name = "Характеристики покемона"
        verbose_name_plural = "Характеристики покемонов"
