from django.urls import path
from.views import FoodListAPIView,OrderAPIView,RegisterAPIView,LoginAPIView,AdminAnalyticsAPIView

urlpatterns = [
    path('foods/',FoodListAPIView.as_view()),
    path('orders/',OrderAPIView.as_view()),
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('analytics/',AdminAnalyticsAPIView.as_view()),
]
