# Generated by Django 5.0.2 on 2024-02-12 18:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('music_file', models.FileField(upload_to='music_files')),
                ('length', models.TimeField(blank=True, null=True)),
                ('replays', models.IntegerField()),
                ('likes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_object_likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
