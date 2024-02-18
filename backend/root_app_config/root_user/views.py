import mimetypes
import os
from urllib.parse import unquote


from django.conf import settings
from django.http import FileResponse


# rest frame work imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


# project imports
from .models import AuthUserModel as User
from .serializer import UserSerializer, RegisterSerializer

#-------------------class based views-------------------------

class UserSignUpAPIView(generics.CreateAPIView):
    """
    Basic api end point to register a  user
    """
    queryset = User
    serializer_class = RegisterSerializer
    

class UserInformationRetrieveAPIView(generics.RetrieveAPIView):
    """
    Basic end point to find a user by user name and send the user back
    """
    lookup_field = 'username'
    queryset = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    """
    Api end point to update user after searching it with it's username

    required field include

        username: str
        password: str
        email: str
    
    other fields are not required
    """
    lookup_field = 'username'
    queryset = User
    serializer_class = UserSerializer
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
    
    if not os.path.exists(f"{settings.MEDIA_ROOT}/music_files/audio/{path}"):
        return Response("No such file exists.", status=404)

    # Guess the MIME type of a file. Like pdf/docx/xlsx/png/jpeg
    mimetype, encoding = mimetypes.guess_type(f"{settings.MEDIA_ROOT}/music_files/audio/{path}", strict=True)
    if not mimetype:
        mimetype = "text/html"

    # By default, percent-encoded sequences are decoded with UTF-8, and invalid
    # sequences are replaced by a placeholder character.
        
    file_path = unquote(os.path.join(f"{settings.MEDIA_ROOT}/music_files/audio/{path}")).encode("utf-8")
    
    return FileResponse(open(file_path, "rb").read(), content_type=mimetype)