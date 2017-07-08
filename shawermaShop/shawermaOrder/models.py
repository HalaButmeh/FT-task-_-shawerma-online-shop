from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@python_2_unicode_compatible  
class MenuItem(models.Model):
	name = models.CharField(max_length=30)
	price = models.DecimalField(decimal_places=2, max_digits=10, default = 0)
	description = models.CharField(max_length=300)
	
	def __str__(self):
		return self.name+": "+ self.description

@python_2_unicode_compatible  
class Order(models.Model):
	address = models.CharField(max_length=300)
	deliveryTime =  models.DateTimeField()
	owner = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
	menuItems = models.ManyToManyField(MenuItem, through='MenuItemToOrder')
	def __str__(self):
		return  self.address+", "+ `self.deliveryTime`

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@python_2_unicode_compatible  
class MenuItemToOrder(models.Model):
	menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	quantity = models.IntegerField(default = 1)

	def __str__(self):
		return self.menuItem.name+", "+ `self.quantity` 
