# Generated by Django 4.2.6 on 2023-10-22 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('word', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('shared', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Swag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
    ]
