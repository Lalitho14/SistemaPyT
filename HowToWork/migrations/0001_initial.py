# Generated by Django 5.1 on 2024-08-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usr', models.CharField(max_length=45, unique=True)),
                ('email', models.CharField(max_length=60, unique=True)),
                ('passwd', models.CharField(max_length=45)),
            ],
        ),
    ]
