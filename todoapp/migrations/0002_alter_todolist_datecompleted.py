# Generated by Django 4.1.5 on 2023-01-30 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]