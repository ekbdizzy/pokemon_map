# Generated by Django 3.1.4 on 2020-12-24 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_templatepokemonentity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PokemonEntity',
        ),
    ]
