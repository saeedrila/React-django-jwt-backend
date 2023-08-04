from rest_framework import serializers
from user.models import NewUser


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields=("username","email","phone","password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = NewUser
        fields=['email','password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'username', 'email','phone','profile')


class ImageupdateSerializer(serializers.ModelSerializer):
    class Meta:
        profile = serializers.ImageField()
        model = NewUser
        fields = ("profile",)