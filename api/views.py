from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token 
from django.db.models import Sum,Count
#

from .models import Food,Order,Restaurant, Payment
from .serializers import FoodSerializer,OrderSerializer,RegisterSerializer,RestaurantSerializer,PaymentSerializer
import uuid

class FoodListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        profile=request.user.userprofile
        if profile.role in ['admin','customer']:
            foods=Food.objects.all()
        else:
            foods=Food.objects.filter(restaurant=profile.restaurant)

        serializer=FoodSerializer(foods,many=True)
        return Response(serializer.data)

    def post(self,request):
        profile = request.user.userprofile

        if profile.role != 'admin':
            return Response(
                {"error":"Only admin can add food"},
                status=403
            )

        serializer = FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)

        return Response(serializer.errors,status=400)
   #
    
class OrderAPIView(APIView):
    permission_classes=[IsAuthenticated]
    #
    def get(self,request):
        profile=request.user.userprofile

        if profile.role=='admin':
            orders=Order.objects.all()
        elif profile.role=='customer':
            orders=Order.objects.filter(user=request.user)
        else:
            orders=Order.objects.filter(restaurant=profile.restaurant)
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        profile=request.user.userprofile
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            food=serializer.validated_data['food']
            if profile.role =="cashier"and food.restaurant != profile.restaurant:
                return Response({"error":"you cannot order food from another restaurant"},status=403)
            quantity=serializer.validated_data['quantity']
            total_price=food.price*quantity
            serializer.save(
                user=request.user,
                restaurant=food.restaurant,
                total_price=total_price
            )
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
   #
        #

class RegisterAPIView(APIView):
    permission_classes= []
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User created successfully"},status=201)
        
        return Response(serializer.errors,status=400)
    
class LoginAPIView(APIView):
    permission_classes= []
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
        
        food_stats=Order.objects.values('restaurant__name','food__name').annotate(
            total_quantity=Sum('quantity'),
            total_earned=Sum('total_price'),
            order_count=Count('id')
        )
        
        return Response({
            "total_orders":total_orders,
            "total_revenue":total_revenue,
            "food_statistics":food_stats
        })
  
class RestaurantListAPIView(APIView):
    permission_classes = []

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)             
    
class RestaurantFoodAPIView(APIView):
    permission_classes = []

    def get(self, request, restaurant_id):
        food_type=request.query_params.get('type')
        foods = Food.objects.filter(restaurant_id=restaurant_id)
        if food_type:
            foods=foods.filter(food_type=food_type)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    
class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        
        if order.payment_method=="cash":
            return Response({"error":"Cash payment does not require online transaction"},status=400)
        import uuid
        # Simulate payment success
        payment = Payment.objects.create(
            order=order,
            payment_method=order.payment_method,
            status="completed",
            transaction_id=str(uuid.uuid4())
        )

        return Response({
            "message": "Payment successful",
            "transaction_id": payment.transaction_id
        })
    
class UpdateOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        profile = request.user.userprofile
        if profile.role not in ['admin', 'owner', 'cashier']:
            return Response({"error": "Not allowed"}, status=403)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ['pending', 'preparing', 'delivered']:
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()

        return Response({"message": "Order status updated"})

