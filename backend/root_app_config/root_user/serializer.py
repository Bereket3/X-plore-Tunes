import os
from uuid import uuid4

# django main imports
from django.contrib.auth import get_user_model

# rest frame work imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# custom made imports
from .validate_password import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User updating serializer

    can take all the fields in the user model and update if the 
    user is authenticated
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'gender',
            'age',
            'premium_user',
            'password',
            'profile_picture'
        ]


    def update(self, instance, validated_data):
        """
        It takes in a request and will update the user

        if a user profile image exists these functions make sure to
        delete it in order not to make multiple files that does't necessarily are
        bing used
        """
        password = validated_data['password']
        try:
            image = validated_data['profile_picture']
        except:
            image = None
        if image:
            image.name = rename_file(image)
            instance.profile_picture.delete()
    

        for key, value in validated_data.items():
            if key == 'profile_picture':
                setattr(instance, key, image)
                continue
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    serializer for creating a new user

    it takes user name, email and password 
    check the existence of the user name and email and
    make a new user

    if there is any error returns response of the error
    """
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
        )

    password2 = serializers.CharField(
        write_only=True, 
        required=True
        )


    class Meta:
        model = User
        fields = [
            'username', 
            'email',
            'gender',
            'age',
            'premium_user',
            'password',
            'password2'
        ]


    def validate(self, attrs):
        """
        Custom validation for password validation and mismatch in password

        return the error as a reponse to the frontend
        """
        password = validate_password(attrs['password'])
        messages = {}
        if password:
            for index, error_type in enumerate(password):
                messages[f'password validation error {index}'] = error_type

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if messages:
            raise serializers.ValidationError({'password':messages})

        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


def rename_file(file):
    """
    Takes in a file and clean it from white space and return the file name with
    file name changed to file name + uuid4 

    it ensure that there will be no duplicates in the data base
    """
    name, extension = os.path.splitext(file.name)
    name = ''.join(name.split())

    return name + '-' + str(uuid4()) + extension