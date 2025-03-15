# Generated by Django 5.1.5 on 2025-03-15 11:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eco', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='point_value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
