# Generated by Django 5.0.6 on 2024-07-03 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library_app', '0005_remove_staffissuedbook_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffissuedbook',
            name='fine',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='studentissuedbook',
            name='fine',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]