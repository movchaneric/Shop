from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
	name= models.CharField(max_length=200, null=True)
	email= models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField()
	digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(null = True, blank=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=True)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	# total cart item QUANTITY
	@property
	def get_cart_total(self):
		total = 0
		orderitems = self.orderitem_set.all()
		for item in orderitems:
			total += item.quantity
		return total

	# total cart item PRICE
	@property
	def get_cart_items(self):
		total = 0
		orderitems = self.orderitem_set.all()
		for item in orderitems:
			total += (item.quantity * item.product.price)
		return total
	

class OrderItem(models.Model):
	order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
	order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
	address= models.CharField(max_length=200, null=True)
	city= models.CharField(max_length=200, null=True)
	state= models.CharField(max_length=200, null=True)
	zipcode= models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address