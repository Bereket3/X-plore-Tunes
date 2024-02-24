import mimetypes
import os
from urllib.parse import unquote


from django.conf import settings
from django.http import FileResponse


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


from .models import MusicContainer as Music
from .serializer import MusicSerializer



class MusicCreateAPIView(generics.CreateAPIView):
    queryset = Music
    serializer_class = MusicSerializer
    # permission_classes = [IsAuthenticated]


class MusicUpdateDeleteAndGetAPIView(generics.DestroyAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Music
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticated]


#-------------------- function based views -----------------------
    

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_media_path(request, path) -> FileResponse:
    """
    The get_media_path function is a helper function that takes in the request and
    path of a file. 
    
    It then checks if the file exists, and returns an error message if
    it does not exist. 
    
    If it does exist, it will return an HttpResponse with the
    correct headers to serve up the media.
    
    @param path: Determine the path of the file to be served
    """
    _range = request.headers['Range']
    _start , _end = _range.split('-')
    _start = int(_start)
    _end = int(_end)
    
    if not os.path.exists(f"{settings.MEDIA_ROOT}/music_files/audio/{path}"):
        return Response("No such file exists.", status=404)

    # Guess the MIME type of a file. Like pdf/docx/xlsx/png/jpeg
    mimetype, encoding = mimetypes.guess_type(f"{settings.MEDIA_ROOT}/music_files/audio/{path}", strict=True)
    if not mimetype:
        mimetype = "text/html"
    
    

    # By default, percent-encoded sequences are decoded with UTF-8, and invalid
    # sequences are replaced by a placeholder character.
        
    file_path = unquote(os.path.join(f"{settings.MEDIA_ROOT}/music_files/audio/{path}")).encode("utf-8")
    
    
    return FileResponse(open(file_path, "rb"), content_type=mimetype)