# Generated by Django 2.2.5 on 2020-01-19 09:30

from django.db import migrations, models
import mySite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mySite', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', mySite.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is_active'),
        ),
    ]