from django.db import models

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
class Order(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
  ]

  order_number = models.CharField(max_length=50, unique=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  customer_name = models.CharField(max_length=200)
  customer_email = models.EmailField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order {self.order_number} - {self.customer_name}"
  

