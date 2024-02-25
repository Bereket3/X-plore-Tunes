import mimetypes


from tinytag import TinyTag

# rest frame work imports
from rest_framework import serializers

# django main imports
from django.contrib.auth import get_user_model


# project imports
from .models import MusicContainer as Music


AUDIO_TYPES = {
        'audio/3gpp',
        'audio/3gpp2',
        'audio/aac',
        'audio/basic',
        'audio/mpeg',
        'audio/opus',
        'audio/x-aiff',
        'audio/x-pn-realaudio',
        'audio/x-wav',
    }


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'owner',
            'title',
            'likes',
            'music_file',
            'length',
            'replays',
            'music_cover_art'
        ]

    
    def validate(self, attrs):
        """
        custome validation to check wather a media file is of type audio

        If not it returns an error response to the frontend
        """
        music_file = attrs['music_file']
        mimetype, encoding = mimetypes.guess_type(music_file.__str__(), strict=True)

        if mimetype not in AUDIO_TYPES:
            raise serializers.ValidationError({"detail": "unsupported file type"})
        
        genre, lenght, samplerate =validate_music(music_file.temporary_file_path())
        attrs['genre'] = genre if genre else 'Any'
        attrs['length'] = lenght
        attrs['sample_rate'] = samplerate
       
        return attrs


def validate_music(music):
    """
    from the music file it extract the genre, length nad samplerate
    """
    tag = TinyTag.get(music)
    return tag.genre, tag.duration, tag.samplerate



class MusicUpdateSerializer(serializers.ModelSerializer):
    model = Music
    fields = [
        'owner',
        'title',
        'likes',
        'music_file',
        'length',
        'replays',
        'music_cover_art'
    ]

    def update(self, instance, validated_data):
        try:
            music_cover = validated_data['music_cover_art']
            music_file = validated_data['music_file']
        except:...
        
        return super().update(instance, validated_data)