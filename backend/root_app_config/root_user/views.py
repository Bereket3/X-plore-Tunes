# rest frame work imports
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from oauth2_provider.models import AccessToken


# project imports
from .models import AuthUserModel as User

from .serializer import (
        UserSerializer, 
        RegisterSerializer,
        TokenValidation
    )

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


class ValidateToken(APIView):
    """
    Custom validating function

    will take in the token and check if it is valid and return true or false
    as a response
    """
    def permission_denied(self, request, message=None, code=None):
        pass

    def post(self, request: Request, *args, **kwargs):
        serialiezer = TokenValidation(data=request.data)
        if serialiezer.is_valid(raise_exception=True):
            token = serialiezer.data['token']
            try:
                token_object = AccessToken.objects.get(token=token)
                if token_object.is_valid():
                    return Response({'message':True})
            except:
                return Response({'message':'This token does not exist in the database'})
        return Response({'massage':False})