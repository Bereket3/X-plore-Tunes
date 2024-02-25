# rest frame work imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
