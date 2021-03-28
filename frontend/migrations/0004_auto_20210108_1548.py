# Generated by Django 3.1.1 on 2021-01-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='pst_image1',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='Hotel Image 1'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='pst_image2',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='Hotel Image 2'),
        ),
    ]