# Generated by Django 3.1.1 on 2021-02-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0020_auto_20210218_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='pst_email',
        ),
        migrations.RemoveField(
            model_name='about',
            name='pst_number',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_number',
            field=models.CharField(max_length=20, verbose_name='Founder Number'),
        ),
    ]
