# Generated by Django 2.0.5 on 2018-05-23 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default=172513612749951490145218030035656885764, max_length=64, unique=True, verbose_name='Hash'),
        ),
    ]
