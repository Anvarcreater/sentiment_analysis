# Generated by Django 5.2 on 2025-05-24 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_orderlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
