from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user

# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self,request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"User Created Successfully",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):

    def post(self,request:Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email,password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message":"Login Successfull",
                #"token":user.auth_token.key,
                # using jwt tokens instead
                "tokens":tokens
            }
            return Response(data=response,status=status.HTTP_200_OK)
        response = {"message":"Invalid user name"}
        return Response(data=response)



    def get(self,request:Request):
        #request.user is a user object that returns the user that makes the request.
        content = {
            "user":"{}".format(request.user),
            "auth":"{}".format(request.auth)
        }
        return Response(data=content,status=status.HTTP_200_OK)

