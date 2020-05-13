# Generated by Django 3.0.1 on 2020-04-24 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novelas', '0004_auto_20200422_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='novelas',
            name='estado',
            field=models.CharField(blank=True, default='En curso', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comentarios',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novelas.allchaps'),
        ),
    ]