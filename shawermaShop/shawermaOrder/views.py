from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem, Order, MenuItemToOrder
from .serializers import ShawermaorderSerializer, OrderSerializer,  UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import generics
from django.db.models import Sum, F, Avg
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db import connection
from django.db.models import DecimalField,FloatField
from rest_framework import viewsets
from django.core import serializers



class Menu(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        menuItems = MenuItem.objects.all()
        serializer = ShawermaorderSerializer(menuItems, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShawermaorderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MenuItemDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        try:
            return MenuItem.objects.get(pk=pk)
    	except MenuItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        menuItem = self.get_object(pk)
        serializer = ShawermaorderSerializer(menuItem)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        menuItem = self.get_object(pk)
        serializer = ShawermaorderSerializer(menuItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        menuItem = self.get_object(pk)
        menuItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
	#User views his orders only
        orders = Order.objects.filter(owner=self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
    def create(self, serializer):
    	serializer.save(owner=self.request.user)

	
    """
    def get_byUser(self, request, format=None):
	orders = Order.objects.all().filter(self.=2006)
	serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
   """


class OrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
    	except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class BestCustomer(APIView):
      def get(self, request, format=None):	
	querySet = MenuItemToOrder.objects.values('order__owner').annotate(total_spending=Sum(F('menuItem__price')*F('quantity'),output_field=DecimalField())).order_by('-total_spending')[:1]
	serializer_class = UserSerializer()
        return Response(list(querySet))

class CustomersAvgSpending(APIView): 
     def get(self, request, format=None):
      	serializer_class = OrderSerializer	
	querySet = MenuItemToOrder.objects.values('order').annotate(orderPrice=Sum(F('quantity') * F('menuItem__price'),output_field=FloatField())).aggregate(amount=Avg(F('orderPrice'),output_field=FloatField()))	
	return Response(querySet)

class CustomersAvgSpendingPerYear(APIView): 
      def get(self, request, year, format=None):
	querySet = MenuItemToOrder.objects.filter(deliveryTime__year = year).values('order__owner').annotate(amount=Avg(F('quantity') * F('menuItem__price'),output_field=FloatField()))
	return Response(list(querySet))

class MonthlyReport(APIView):
      def get(self, request, year,format=None):
      	truncate_date = connection.ops.date_trunc_sql('month', 'deliveryTime')
	records = MenuItemToOrder.objects.filter(order__deliveryTime__year = year).extra({'month':truncate_date}).values('month').annotate(total_revenue=Sum(F('menuItem__price')*F('quantity'),output_field=FloatField()))
	#records = MenuItemToOrder.objects.filter(order__deliveryTime__year = year).values('order__deliveryTime__month').annotate(total_revenue=Sum(F('menuItem__price')*F('quantity'),output_field=FloatField()))
	return Response(list(records))




		

