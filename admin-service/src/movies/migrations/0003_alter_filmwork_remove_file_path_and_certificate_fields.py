# Generated by Django 3.2 on 2022-07-04 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_filmwork_add_file_path_and_certificate_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='filmwork',
            name='file_path',
        ),
    ]
