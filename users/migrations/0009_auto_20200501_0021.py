# Generated by Django 3.0.1 on 2020-05-01 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novelas', '0009_auto_20200501_0021'),
        ('users', '0008_auto_20200428_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='historial',
            field=models.ManyToManyField(to='novelas.allchaps'),
        ),
    ]