from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .serializers import UserRegisterSerializer,Resetserializer,Resetpasswordserializer
from django.urls import reverse
from .services import send_verfication_mail,reset_email
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(CreateAPIView):
    serializer_class=UserRegisterSerializer

    def perform_create(self,serializer):
        user=serializer.save()

        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)

        activate_path=reverse('activate',
                              kwargs={'uid64':uid,
                                      'token':token})
        
        activate_link=f"{self.request.scheme}://{self.request.get_host()}{activate_path}"

        send_verfication_mail(user,activate_link)



class Activateview(APIView):
    
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except:
            return Response({
                "error":"invalid data"
            },status=status.HTTP_400_BAD_REQUEST)
        
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return Response({"message":"your account is active"},status=status.HTTP_200_OK) 
        else:
            return Response({
                "error":"invalid data"
            },status=status.HTTP_400_BAD_REQUEST)


class Logoutapiview(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            refresh_token=request.data.get('refresh')
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"finally Logout the session"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message':'Invaild Details'})
        

class Resetview(APIView):
    def post(self,request):
        serializer=Resetserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data.get('email')
        try:
            user=User.objects.get(email=email)

            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)

            activate_path=reverse('resetpassword',
                                  kwargs={
                                      "uid64":uid,
                                      "token":token
                                  })
            activate_link=f"{self.request.scheme}://{self.request.get_host()}{activate_path}"
            print(activate_link)
            reset_email(user,activate_link)
            return Response({'message':'Password reset email sent successfully'},status=status.HTTP_200_OK)
        except:
            return Response({'message':'email is not found'},status=status.HTTP_400_BAD_REQUEST)

class Resetpasswordview(APIView):
    permission_classes=[AllowAny]
    def get(self,request,uid64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uid64))
            user=User.objects.get(pk=uid)
        except:
            return Response({'message':'invalid response'},status=status.HTTP_401_UNAUTHORIZED)
        
        if default_token_generator.check_token(user,token):
            return Response({'message':'token valid'},status=status.HTTP_202_ACCEPTED)
    def post(self,request,uid64,token):
        serializer=Resetpasswordserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid=force_str(urlsafe_base64_decode(uid64))
            user=User.objects.get(pk=uid)
        except:
            return Response({'message':'invalid response'},status=status.HTTP_401_UNAUTHORIZED)
        
        if default_token_generator.check_token(user,token):
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            return Response({'message':'password updated'},status=status.HTTP_202_ACCEPTED)
        return Response({'message':'invalid response'},status=status.HTTP_401_UNAUTHORIZED)

