from .models import MenuItem,Order, MenuItemToOrder
from rest_framework import serializers
from django.contrib.auth.models import User
 
 
class ShawermaorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('name', 'price' , 'description')

class MenuItemToOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuItemToOrder
        fields = ('id', 'menuItem', 'order' ,'quantity')

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Order
        fields = ('id', 'menuItems' , 'address' , 'deliveryTime' , 'owner')

class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'orders')





	
