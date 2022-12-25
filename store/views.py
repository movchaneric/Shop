from django.shortcuts import render
from .models import *

from django.http import JsonResponse
import json
import datetime

# Create your views here.


def store(request):
	# logged in user check
	if request.user.is_authenticated:
		customer = request.user.customer
		# create an order or query the order if already created
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get all order item that parent(order) has
		items = order.orderitem_set.all()
		orderItems = order.get_cart_total
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		orderItems = order['get_cart_total']


	products = Product.objects.all()
	context = {'products':products,'order':order,'orderItems':orderItems}
	return render(request, 'store/store.html', context)


def cart(request):
	# logged in user check
	if request.user.is_authenticated:
		customer = request.user.customer
		# create an order or query the order if already created
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get all order item that parent(order) has
		items = order.orderitem_set.all()
		orderItems = order.get_cart_total
	else:
		# if cookie cart get deleted from browser create dummy cookie
		try:
			# get cookie from browser and turn cart js dictionary into python dictionary
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		print('Cart: ', cart)

		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		orderItems = order['get_cart_total']

		for i in cart:
			orderItems += cart[i]['quantity']

			product = Product.objects.get(id=i)

			total = (product.price * cart[i]['quantity'])

			order['get_cart_items'] += total
			order['get_cart_total'] += cart[i]['quantity']

			item = {'product':{
			'id':product.id,
			'name':product.name,
			'price':product.price,
			'image':product.image
			},
			'quantity':cart[i]['quantity'],	
			'get_total':total
			} 
			items.append(item)

			# phycal item
			if product.digital == False:
				# show shipping form
				order['shipping'] = True
	
	
	context = {'items':items ,'order':order,'orderItems':orderItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	# logged in user check
	if request.user.is_authenticated:

		customer = request.user.customer
		# create an order or query the order if already created
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get all order item that parent(order) has
		items = order.orderitem_set.all()
		orderItems = order.get_cart_total

	else:

		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

			print('CART:' , cart)

		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		orderItems = order['get_cart_total']

		for i in cart:
			# cart logo update
			orderItems += cart[i]['quantity']

			product = Product.objects.get(id=i)

			total = (product.price * cart[i]['quantity'])

			order['get_cart_items'] += total
			order['get_cart_total'] += cart[i]['quantity']

			item = {'product':{
			'id':product.id,
			'name':product.name,
			'price':product.price,
			'image':product.image
			},
			'quantity':cart[i]['quantity'],	
			'get_total':total
			} 
			items.append(item)

			# phycal item
			if product.digital == False:
				# show shipping form
				order['shipping'] = True
	
	context = {'items':items , 'order':order, 'orderItems':orderItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	
	productId = data['productId']
	action = data['action']

	print('productId: ', productId)
	print('action: ', action)

	customer = request.user.customer

	# get clicked product id
	product = Product.objects.get(id = productId)

	# create or get created order and just modifie it 
	order, created = Order.objects.get_or_create(customer = customer, complete=False)

	# create or get created orderItems and just modifie it
	orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

	if action == 'add':
		orderItem.quantity = orderItem.quantity + 1
	elif action == 'remove':
		orderItem.quantity = orderItem.quantity - 1

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added..', safe=False)


def processOrder(request):
	# create random order id using timestamp()
	transaction_id = datetime.datetime.now().timestamp()

	# load data from process-order JsonResponse
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_items:
			order.complete = True

		order.save()

		if order.checkShipment == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address = data['shippingForm']['address'],
				city = data['shippingForm']['city'],
				state = data['shippingForm']['state'],
				zipcode = data['shippingForm']['zipcode']
				)
	else:
		print ("User is not authenticated")
		print('COOKIE', request.COOKIES)

		name = data['form']['name']
		email = data['form']['email']

		customer, created = Customer.objects.get_or_create(email=email)
		# if customer wants to use the same email but different name
		customer.name = name
		customer.save()

	return JsonResponse('payment submitted...', safe= False)









