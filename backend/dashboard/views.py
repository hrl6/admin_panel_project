from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  filterset_fields = ['name', 'price', 'stock']
  search_fields = ['name', 'description']

class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  filterset_fields = ['status', 'order_number']
  search_fields = ['order_number', 'customer_details']

