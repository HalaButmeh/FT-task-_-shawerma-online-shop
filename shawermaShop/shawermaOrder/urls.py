from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    	url(r'^mneuItems/$', views.Menu.as_view()),
    	url(r'^mneuItems/(?P<pk>[0-9]+)$', views.MenuItemDetail.as_view()),
	url(r'^orders/$', views.OrderList.as_view()),
	url(r'^orders/(?P<pk>[0-9]+)$', views.OrderDetail.as_view()),
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
	url(r'^bestCustomer/$', views.BestCustomer.as_view()),
	url(r'^avgSpending/$', views.CustomersAvgSpending.as_view()),
	url(r'^avgSpendingPerYear/(?P<year>[0-9]+)/$', views.CustomersAvgSpendingPerYear.as_view()),
	url(r'^report/(?P<year>[0-9]+)/$', views.MonthlyReport.as_view()),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)
