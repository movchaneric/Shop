from django.shortcuts import render
from .models import *

# Create your views here.


def store(request):
	products = Product.objects.all()
	context = {'products':products,}
	return render(request, 'store/store.html', context)


def cart(request):
	# logged in user check
	if request.user.is_authenticated:
		customer = request.user.customer
		# create an order or query the order if already created
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get all order item that parent(order) has
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
	
	context = {'items':items ,'order':order}
	return render(request, 'store/cart.html', context)


def checkout(request):
	# logged in user check
	if request.user.is_authenticated:
		customer = request.user.customer
		# create an order or query the order if already created
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get all order item that parent(order) has
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
	
	context = {'items':items ,'order':order}
	return render(request, 'store/checkout.html', context)
