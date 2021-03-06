# Generated by Django 3.0.2 on 2020-04-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, verbose_name='아이디')),
                ('password', models.CharField(max_length=64, verbose_name='비밀번호')),
                ('registered', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
            ],
        ),
    ]
