# Generated by Django 5.1.5 on 2025-03-15 22:17

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=750)),
                ('point_value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EducationalLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('category', models.CharField(choices=[('general', 'General Sustainability & Green Living'), ('zero_waste', 'Zero Waste & Minimalism'), ('ethical_brands', 'Eco-Friendly Shopping & Ethical Brands'), ('green_energy', 'Green Energy & Sustainable Homes'), ('lifestyle', 'Ecofriendly Lifestyle'), ('recycling', 'Recycling')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Submitted_Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='No title provided.', max_length=128)),
                ('description', models.TextField(default='No description provided.', max_length=750)),
                ('point_value', models.IntegerField(default=0)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_Challenge_Log_Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_logged', models.DateTimeField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eco.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(through='Eco.User_Challenge_Log_Entry', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
