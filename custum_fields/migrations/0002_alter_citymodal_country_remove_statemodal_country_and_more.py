# Generated by Django 5.0.4 on 2024-04-09 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custum_fields', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citymodal',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custum_fields.countrymodel'),
        ),
        migrations.RemoveField(
            model_name='statemodal',
            name='country',
        ),
        migrations.AddField(
            model_name='statemodal',
            name='country',
            field=models.ManyToManyField(related_name='states', to='custum_fields.countrymodel'),
        ),
    ]
