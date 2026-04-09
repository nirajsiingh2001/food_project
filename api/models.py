from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    FOOD_TYPE=(
        ('veg','Veg'),
        ('nonveg','Non Veg')
    )
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="foods")
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    description=models.TextField()

    food_type=models.CharField(max_length=10,choices=FOOD_TYPE)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    PAYMENT_CHOICES=(
        ('cash','Cash'),
        ('online','Online'),
        ('card','Card'),
        ('upi','UPI')
    )
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('preparing','Preparing'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    payment_method=models.CharField(max_length=10,choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ordered {self.food.name}"
    
class UserProfile(models.Model):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('owner','Owner'),
        ('cashier','Cashier'),
        ('customer','customer')
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True,blank=True)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Payment(models.Model):
    PAYMENT_STATUS=(
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed')
    )
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name="payment")
    payment_method=models.CharField(max_length=10,choices=Order.PAYMENT_CHOICES)
    status=models.CharField(max_length=20,choices=PAYMENT_STATUS,default='pending')
    transaction_id=models.CharField(max_length=100,blank=True,null=True)
    paid_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"