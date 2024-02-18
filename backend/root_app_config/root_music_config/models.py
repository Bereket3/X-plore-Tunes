from typing import Any
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class MusicContainer(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'music_owner')
    title = models.CharField(max_length = 200)
    likes = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'music_object_likes', blank = True, null=True)
    stream = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = 'music_total_stream')
    music_file = models.FileField(upload_to='music_files/audio/')
    length = models.TimeField(blank = True, null = True)
    replays = models.IntegerField(default = 0, blank =True, null = True)
    sample_rate = models.FloatField( default = 0.0)
    genre = models.CharField(max_length = 128, default = '')
    music_cover_art = models.ImageField(upload_to='music_files/cover_art/',null = True, blank= True, default= None)

    created = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
 

    def __str__(self) -> str:
        return self.title
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        self.music_cover_art.delete()
        self.music_file.delete()
        return super().delete(using, keep_parents)