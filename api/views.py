from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token 
from django.db.models import Sum,Count
#

from .models import Food,Order
from .serializers import FoodSerializer,OrderSerializer,RegisterSerializer

class FoodListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        foods=Food.objects.all()
        serializer=FoodSerializer(foods,many=True)
        return Response(serializer.data)
    def post(self,request):
        if not request.user.is_staff:
            return Response({"error":"only admin can add food"},status=403)
        serializer=FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
class OrderAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        orders=Order.objects.filter(user=request.user)
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            food=serializer.validated_data['food']
            quantity=serializer.validated_data['quantity']
            
            total_price=food.price*quantity
            
            serializer.save(user=request.user,total_price=total_price)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
        #

class RegisterAPIView(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User created successfully"},status=201)
        
        return Response(serializer.errors,status=400)
    
class LoginAPIView(APIView):
    permission_classes=[]
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        
        user=authenticate(username=username,password=password)
        
        if user:
            token,created=Token.objects.get_or_create(user=user)
            return Response({"token":token.key})
        
        return Response({"error":"Invalid credentials"},status=400)
    
class AdminAnalyticsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        
        if not request.user.is_staff:
            return Response(
                {"error":"only admin can view analytics"},status=403
            )
            
        total_orders=Order.objects.count()
        total_revenue=Order.objects.aggregate(
            total=Sum('total_price')
        )['total']or 0
        
        food_stats=Order.objects.values('food__name').annotate(
            total_quantity=Sum('quantity'),
            total_earned=Sum('total_price'),
            order_count=Count('id')
        )
        
        return Response({
            "total_orders":total_orders,
            "total_revenue":total_revenue,
            "food_statistics":food_stats
        })
            
            