# Generated by Django 5.0.2 on 2024-02-11 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authusermodel',
            name='is_active',
        ),
    ]
