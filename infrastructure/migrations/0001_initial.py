# Generated by Django 5.1.1 on 2024-09-07 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Environnement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='environnements', to='infrastructure.departement')),
            ],
        ),
        migrations.CreateModel(
            name='Serveur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=15)),
                ('domain', models.CharField(max_length=255)),
                ('environnement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serveurs', to='infrastructure.environnement')),
            ],
        ),
        migrations.CreateModel(
            name='ServeurRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serveurs', to='infrastructure.role')),
                ('serveur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='infrastructure.serveur')),
            ],
        ),
    ]
