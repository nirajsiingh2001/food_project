from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="foods")
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    description=models.TextField()
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    ordered_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ordered {self.food.name}"