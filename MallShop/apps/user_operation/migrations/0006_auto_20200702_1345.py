# Generated by Django 3.0.7 on 2020-07-02 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0005_auto_20200701_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='province',
            field=models.CharField(default='', max_length=100, verbose_name='省份'),
        ),
    ]