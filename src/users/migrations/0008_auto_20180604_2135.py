# Generated by Django 2.0.5 on 2018-06-04 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180603_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(default=124092968277571734793361125887098456054, max_length=128, unique=True, verbose_name='Hash'),
        ),
    ]
