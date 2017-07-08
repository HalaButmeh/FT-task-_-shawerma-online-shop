from django.contrib import admin

from .models import MenuItem, Order, MenuItemToOrder

admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(MenuItemToOrder)
