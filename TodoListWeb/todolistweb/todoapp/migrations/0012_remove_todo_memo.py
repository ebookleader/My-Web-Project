# Generated by Django 3.0.2 on 2020-05-12 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0011_todo_date_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='memo',
        ),
    ]
