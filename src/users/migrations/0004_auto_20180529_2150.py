# Generated by Django 2.0.5 on 2018-05-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180523_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default=40456589173735002276672786456201180347, max_length=128, unique=True, verbose_name='Hash'),
        ),
    ]
