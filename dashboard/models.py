from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
def generate_order_number():
  return str(uuid.uuid4()).split('-')[0].upper()

class Product(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(help_text="Detailed description of the product")
  price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  stock = models.IntegerField(validators=[MinValueValidator(0)], help_text="Current stock quantity")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def clean(self):
    if self.price < 0:
      raise ValidationError('Price cannot be negative')
    if self.stock < 0:
      raise ValidationError('Stock cannot be negative')

  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['-created_at']
    verbose_name = 'Product'
    verbose_name_plural = 'Products'
  
class Order(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
  ]

  order_number = models.CharField(max_length=50, unique=True, default=generate_order_number, editable=False)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  customer_name = models.CharField(max_length=200)
  customer_email = models.EmailField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  created_at = models.DateTimeField(auto_now_add=True)
  notes = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"Order {self.order_number} - {self.customer_name}"
  
  class Meta:
    ordering = ['-created_at']
    verbose_name = 'Order'
    verbose_name_plural = 'Orders'
