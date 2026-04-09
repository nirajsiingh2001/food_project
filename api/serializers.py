from rest_framework import serializers
from .models import Food,Order, Payment,Restaurant
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food.name", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model=Order
        fields=[
            "id","food","food_name","restaurant","restaurant_name","quantity","total_price","username","ordered_at","payment_method","status"
        ]
        read_only_fields=['username','total_price','ordered_at','restaurant','status']

    def create(self,validated_data):
        food=validated_data['food']
        quantity=validated_data['quantity']
        validated_data['total_price']=food.price*quantity
        return super().create(validated_data)
        
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

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurant
        fields="__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
        read_only_fields=['status','transaction_id']
        