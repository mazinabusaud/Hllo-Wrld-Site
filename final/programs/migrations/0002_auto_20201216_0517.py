# Generated by Django 3.1.4 on 2020-12-16 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]