# Generated by Django 3.2.6 on 2021-09-07 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20210908_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.CharField(max_length=64),
        ),
    ]