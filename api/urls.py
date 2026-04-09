from django.urls import path
from.views import FoodListAPIView,OrderAPIView, PaymentAPIView,RegisterAPIView,LoginAPIView,AdminAnalyticsAPIView,RestaurantListAPIView,RestaurantFoodAPIView, UpdateOrderStatusAPIView

urlpatterns = [
    path('foods/',FoodListAPIView.as_view()),
    path('orders/',OrderAPIView.as_view()),
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('analytics/',AdminAnalyticsAPIView.as_view()),
    path('restaurants/',RestaurantListAPIView.as_view()),
    path('restaurants/<int:restaurant_id>/foods/',RestaurantFoodAPIView.as_view()),
    path('payment/',PaymentAPIView.as_view()),
    path('orders/<int:order_id>/status/',UpdateOrderStatusAPIView.as_view())]


