# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-20 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wyniki_2017', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateprecinctvotes',
            name='candidate',
        ),
        migrations.RemoveField(
            model_name='candidateprecinctvotes',
            name='precinct',
        ),
        migrations.AddField(
            model_name='precinct',
            name='valid_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_1',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_10',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_11',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_12',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_2',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_3',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_4',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_5',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_6',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_7',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_8',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_9',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='precinct',
            name='votes_cast',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='allowed',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='cards_issued',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='precinct',
            name='invalid_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Candidate',
        ),
        migrations.DeleteModel(
            name='CandidatePrecinctVotes',
        ),
    ]