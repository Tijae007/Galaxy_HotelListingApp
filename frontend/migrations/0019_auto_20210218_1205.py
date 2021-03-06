# Generated by Django 3.1.1 on 2021-02-18 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0018_remove_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='pst_email',
            field=models.EmailField(default=1, max_length=150, verbose_name='Founder Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='about',
            name='pst_number',
            field=models.IntegerField(default=1, max_length=150, verbose_name='Founder Contact'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_email',
            field=models.EmailField(default=1, max_length=150, verbose_name='Founder Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_number',
            field=models.IntegerField(default=1, max_length=150, verbose_name='Founder Contact'),
            preserve_default=False,
        ),
    ]
