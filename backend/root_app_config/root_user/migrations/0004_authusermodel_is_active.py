# Generated by Django 5.0.2 on 2024-02-11 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root_user', '0003_rename_user_name_authusermodel_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='authusermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
