from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, 
                                     min_length=8, 
                                     style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True, 
                                             min_length=8, 
                                             style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password_repeat']

    def validate(self, data):
        password = data.get('password')
        password_repeat = data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_repeat', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'profile_picture')
        read_only_fields = ('username', 'profile_picture')
