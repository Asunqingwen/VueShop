# Generated by Django 3.0.7 on 2020-07-01 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0004_auto_20200701_1405'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set(),
        ),
    ]
