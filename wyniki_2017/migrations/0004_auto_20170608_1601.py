# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wyniki_2017', '0003_auto_20170420_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wyniki_2017.District'),
        ),
        migrations.AlterField(
            model_name='district',
            name='voivodeship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wyniki_2017.Voivodeship'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='address',
            field=models.CharField(max_length=64, verbose_name='Adres obwodu'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='allowed',
            field=models.PositiveIntegerField(default=0, verbose_name='Dopuszczeni do głosowania'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='cards_issued',
            field=models.PositiveIntegerField(default=0, verbose_name='Karty wydane'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='commune',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wyniki_2017.Commune'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='invalid_votes',
            field=models.PositiveIntegerField(default=0, verbose_name='Nieważne głosy'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='num',
            field=models.PositiveIntegerField(default=0, verbose_name='Numer obwodu w gminie'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='valid_votes',
            field=models.PositiveIntegerField(default=0, verbose_name='Ważne głosy'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_1',
            field=models.PositiveIntegerField(default=0, verbose_name='Grabowski Dariusz Maciej'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_10',
            field=models.PositiveIntegerField(default=0, verbose_name='Pawłowski Bogdan'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_11',
            field=models.PositiveIntegerField(default=0, verbose_name='Wałęsa Lech'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_12',
            field=models.PositiveIntegerField(default=0, verbose_name='Wilecki Tadeusz Adam'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_2',
            field=models.PositiveIntegerField(default=0, verbose_name='Ikonowicz Piotr'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_3',
            field=models.PositiveIntegerField(default=0, verbose_name='Kalinowski Jarosław'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_4',
            field=models.PositiveIntegerField(default=0, verbose_name='Korwin - Mikke Janusz'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_5',
            field=models.PositiveIntegerField(default=0, verbose_name='Krzaklewski Marian'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_6',
            field=models.PositiveIntegerField(default=0, verbose_name='Kwaśniewski Aleksander'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_7',
            field=models.PositiveIntegerField(default=0, verbose_name='Lepper Andrzej'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_8',
            field=models.PositiveIntegerField(default=0, verbose_name='Łopuszański Jan'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_9',
            field=models.PositiveIntegerField(default=0, verbose_name='Olechowski Andrzej Marian'),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='votes_cast',
            field=models.PositiveIntegerField(default=0, verbose_name='Oddane głosy'),
        ),
    ]
