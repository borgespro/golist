# Generated by Django 2.0.5 on 2018-05-30 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180529_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default=89009705023580142031411155250203518503, max_length=128, unique=True, verbose_name='Hash'),
        ),
    ]