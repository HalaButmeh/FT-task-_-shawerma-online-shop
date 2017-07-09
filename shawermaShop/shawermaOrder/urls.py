from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    	url(r'^menuItems/$', views.Menu.as_view(), name='menuItems'),
    	url(r'^menuItems/(?P<pk>[0-9]+)$', views.MenuItemDetail.as_view(), name='menuItemDetail'),
	url(r'^orders/$', views.OrderList.as_view(), name='orders'),
	url(r'^orders/(?P<pk>[0-9]+)$', views.OrderDetail.as_view(), name='orderDetail'),
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^bestCustomer/$', views.BestCustomer.as_view(), name='bestCustomer'),
	url(r'^avgSpending/$', views.CustomersAvgSpending.as_view(), name="avgSpendingPerCustomer"),
	url(r'^avgSpendingPerYear/(?P<year>[0-9]+)/$', views.CustomersAvgSpendingPerYear.as_view(), name="avgSpendingPerCustomerInYear"),
	url(r'^report/(?P<year>[0-9]+)/$', views.MonthlyReport.as_view(),name="monthlyReport"),
	url(r'^menuItemToOrder/$', views.MenuItemToOrderView.as_view(),name="menuItemToOrder"),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)
