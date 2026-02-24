from rest_framework import serializers
from .models import Food,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        read_only_fields=['user','ordered_at']
        
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user