from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True,
                                   min_length=8,
                                   validators=[validate_password])
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model= User
        fields=('first_name','last_name','email','username','phone_number','password','password2')

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('the password is not match')
        
        return attrs
    
    def create(self,validate_data):
        validate_data.pop('password2')
        password=validate_data.pop('password')
        user=User.objects.create_user(password=password, **validate_data)
        return user
    
class Resetserializer(serializers.Serializer):
    email=serializers.EmailField()

class Resetpasswordserializer(serializers.Serializer):
   
    password=serializers.CharField(style={'input_type':'password'},write_only=True,min_length=8,validators=[validate_password])
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('password is not match')
        return super().validate(attrs)