# Generated by Django 3.0.2 on 2020-04-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_auto_20200421_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
