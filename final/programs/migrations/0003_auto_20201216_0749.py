# Generated by Django 3.1.4 on 2020-12-16 07:49

from django.db import migrations, models
import programs.models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20201216_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='upload',
            field=models.FileField(default=0, upload_to='documents/', validators=[programs.models.validate_file_extension]),
            preserve_default=False,
        ),
    ]