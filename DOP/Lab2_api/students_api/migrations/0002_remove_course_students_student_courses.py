# Generated by Django 4.2 on 2023-04-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='students_api.course'),
        ),
    ]