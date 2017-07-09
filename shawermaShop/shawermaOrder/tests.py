from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from .models import MenuItem, Order
from rest_framework.authtoken.models import Token
from django.test.client import RequestFactory
from .serializers import ShawermaorderSerializer, OrderSerializer,  UserSerializer
from . import views
import json
#from requests.auth import HTTPBasicAuth


class MenuTests(APITestCase):
    
    def test_create_menuItems(self):

        User.objects.create_superuser('admin','admin@test.com','P@ssword123')
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)	        
	self.assertEqual(User.objects.count(), 1)
	url = reverse('shawermaOrder:menuItems')
	data = {"name": "Item1","price":"10","description":"This is the first sandwitch"}		    
	response = self.client.post(url, data, format='json')

	data = {'name': 'Item2','price':'15','description':'This is the second sandwitch'}		    
	response = self.client.post(url, data, format='json')
	
	data = {'name': 'Item3','price':'20','description':'This is the third sandwitch'}		    
	response = self.client.post(url, data, format='json')
	
	data = {'name': 'Item4','price':'15','description':'This is the fourth sandwitch'}		    
	response = self.client.post(url, data, format='json')
	response = self.client.get(url)

	self.assertEqual(response.status_code, 200)
	self.assertEqual(MenuItem.objects.count(), 4)

class OrderTests(APITestCase):
    def test_manageOrder(self):  
	User.objects.create_superuser('admin','admin@test.com','P@ssword123')
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)	        

	url = reverse('shawermaOrder:menuItems')
	data = {"name": "Item1","price":"20","description":"This is the first sandwitch"}		    
	response = self.client.post(url, data, format='json')

	data = {'name': 'Item2','price':'15','description':'This is the second sandwitch'}		    
	response = self.client.post(url, data, format='json')
	
	data = {'name': 'Item3','price':'13','description':'This is the third sandwitch'}		    
	response = self.client.post(url, data, format='json')
	
	data = {'name': 'Item4','price':'15','description':'This is the fourth sandwitch'}		    
	response = self.client.post(url, data, format='json')
	response = self.client.get(url)


	user = User.objects.create(id='2',username='user1');
	user.set_password('Password')
	user.save() 

	user=User.objects.create(id='3',username='user2');
	user.set_password('Password')
	user.save() 
	self.assertEqual(User.objects.count(), 3)

	#Authinticate user1	
	token = Token.objects.get(user__username='user1')
	self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
	#login with user1	
	response=self.client.login(username='user1', password='Password')
	self.assertTrue(response)
	user = User.objects.get(username='user1')

	#user1 make orders
	url = reverse('shawermaOrder:orders')
	menuItemOrderUrl = reverse('shawermaOrder:menuItemToOrder')

	response = self.client.post(url,{
		"address": "Ramallah",
		"deliveryTime": "2017-08-01T13:00:00Z"}, format='json')
	response = self.client.post(menuItemOrderUrl,{
		"order": "1",
		"menuItem": "1",
		"quantity" : "2"}, format='json')
	response = self.client.post(menuItemOrderUrl,{
		"order": "1",
		"menuItem": "2",
		"quantity" : "3"}, format='json')
	

	response = self.client.post(url,{
		"address": "Ramallah",
		"deliveryTime": "2017-07-01T13:00:00Z"}, format='json')
	response = self.client.post(menuItemOrderUrl,{
		"order": "2",
		"menuItem": "3",
		"quantity" : "2"}, format='json')

	
	#get orders for user1	
	response = self.client.get(url,format='application/json')	
	self.assertEqual(json.dumps(response.data), '[{"id": 1, "menuItems": [1, 2], "address": "Ramallah", "deliveryTime": "2017-08-01T13:00:00Z", "owner": "user1"}, {"id": 2, "menuItems": [3], "address": "Ramallah", "deliveryTime": "2017-07-01T13:00:00Z", "owner": "user1"}]')

	self.client.logout();


	#Authinticate user2	
	token = Token.objects.get(user__username='user2')
	self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
	#login with user1	
	response=self.client.login(username='user2', password='Password')
	self.assertTrue(response)
	user = User.objects.get(username='user2')

	#user2 make orders
	url = reverse('shawermaOrder:orders')
	response = self.client.post(url,{
		"address": "Ramallah",
		"deliveryTime": "2017-09-01T13:00:00Z"}, format='json')
	response = self.client.post(menuItemOrderUrl,{
		"order": "3",
		"menuItem": "3",
		"quantity" : "3"}, format='json')


	
	#get orders for user2	
	response = self.client.get(url)
	
	self.assertEqual(json.dumps(response.data), '[{"id": 3, "menuItems": [3], "address": "Ramallah", "deliveryTime": "2017-09-01T13:00:00Z", "owner": "user2"}]')
	
	self.client.logout();
	
	

	#admin login
	token = Token.objects.get(user__username='admin')
	self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
	response=self.client.login(username='admin', password='P@ssword123')
	self.assertTrue(response)

	
	#get best customer	
	url = reverse('shawermaOrder:bestCustomer')
	response = self.client.get(url)
	self.assertEqual(response.data, [{'total_spending': 111.0, 'order__owner': 2}])

	
	#get total avg spending per customer	
	url=reverse('shawermaOrder:avgSpendingPerCustomer')
	response = self.client.get(url)
	self.assertEqual(response.data,  [{'amount': 37.0, 'order__owner': 2}, {'amount': 39.0, 'order__owner': 3}])	

	#get avg spending per customer in 2017
	url=reverse('shawermaOrder:avgSpendingPerCustomerInYear', args=[2017])
	response = self.client.get(url)
	self.assertEqual(response.data, [{'amount': 37.0, 'order__owner': 2}, {'amount': 39.0, 'order__owner': 3}])	
	

	
	#get revenue monthly report
	url = reverse('shawermaOrder:monthlyReport',args=[2017])
	response = self.client.get(url)
	self.assertEqual(response.data, [{'total_revenue': 26.0, 'month': u'2017-07-01'}, {'total_revenue': 85.0, 'month': u'2017-08-01'}, {'total_revenue': 39.0, 'month': u'2017-09-01'}])
	self.client.logout();
	
	
	

	
		


	

