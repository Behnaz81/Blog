from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from users.serializers import RegisterSerializer, LoginSerializer 

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({'user': serializer.data, 'token': token.key}, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)

                return Response({'user': serializer.data, 
                                 'token': token.key}, 
                                 status=status.HTTP_200_OK)
            
            return Response({'details':'Invalid data'}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
