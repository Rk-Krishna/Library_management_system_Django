# Generated by Django 5.0.6 on 2024-07-02 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library_app', '0002_user_is_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffissuedbook',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='studentissuedbook',
            name='student',
        ),
        migrations.AddField(
            model_name='staffissuedbook',
            name='staff_id',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentissuedbook',
            name='student_register_no',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffissuedbook',
            name='book',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='studentissuedbook',
            name='book',
            field=models.CharField(max_length=100),
        ),
    ]