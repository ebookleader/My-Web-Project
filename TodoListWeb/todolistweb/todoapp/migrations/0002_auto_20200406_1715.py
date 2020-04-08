# Generated by Django 3.0.2 on 2020-04-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Custom User', 'verbose_name_plural': 'Custom User'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='undefine@example.com', max_length=128, verbose_name='이메일'),
            preserve_default=False,
        ),
    ]