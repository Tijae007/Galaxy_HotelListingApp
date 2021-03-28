# Generated by Django 3.1.1 on 2021-02-18 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0019_auto_20210218_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_email',
            field=models.EmailField(max_length=150, verbose_name='Founder Email'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_number',
            field=models.IntegerField(max_length=150, verbose_name='Founder Number'),
        ),
    ]
