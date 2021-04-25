from typing import Optional

import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # tooltip=name,  # disable tooltip because of folium encoding bug
        icon=icon,
    ).add_to(folium_map)


def _get_image_url_or_none(instance) -> str:
    if instance.image:
        return instance.image.url
    return ''


def _create_evolution_description(request, instance) -> Optional[dict]:
    if instance:
        return {
            "title_ru": instance.title_ru,
            "pokemon_id": instance.id,
            "img_url": request.build_absolute_uri(instance.image.url)
        }
    return


def show_all_pokemons(request):
    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': _get_image_url_or_none(pokemon),
            'title_ru': pokemon.title_ru,
        })

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map,
            entity.lat, entity.lon, request.build_absolute_uri(entity.pokemon.image.url))

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map,
            pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    previous_evolution = requested_pokemon.previous_evolution
    next_evolution = Pokemon.objects.filter(previous_evolution=requested_pokemon).first()

    pokemon = {
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "previous_evolution": _create_evolution_description(request, previous_evolution),
        "next_evolution": _create_evolution_description(request, next_evolution),
    }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
