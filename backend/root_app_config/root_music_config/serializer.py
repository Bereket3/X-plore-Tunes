from tinytag import TinyTag

# rest frame work imports
from rest_framework import serializers

# django main imports
from django.contrib.auth import get_user_model


# project imports
from .models import MusicContainer as Music



class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'owner',
            'title',
            'likes',
            'music_file',
            'length',
            'replays'
        ]

    def validate(self, attrs):
        music = attrs['music_file']
        validate_music(music.temporary_file_path())
        return super().validate(attrs)
    
    
    def create(self, validated_data):
        return Music.objects.create(**validated_data)



def validate_music(music):
    tag = TinyTag.get(music)
    print(tag)

