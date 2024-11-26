from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET'])
def your_api_view(request):
    response = Response({'message': 'Success'})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
    # if request.method == 'OPTIONS':
    #     return Response(status=200)
    # return Response({
    #     'products': f"{request.scheme}://{request.get_host()}/api/products/",
    #     'orders': f"{request.scheme}://{request.get_host()}/api/orders/"
    # })

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

