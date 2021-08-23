from django.db import models
import datetime
from datetime import date


from apps.datatables.models import Student, Membership
from apps.accounts.models import *

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Customer(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
 
    #Reccurring payments
    paid_until = models.DateField(null=True, blank=True)
 
    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            # input date as timestamp integer
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            # input date as timestamp string
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(
        self,
        current_date=datetime.date.today()
    ):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until




class Product(models.Model):   
    
    name = models.CharField(max_length=30)
    isdigital = models.BooleanField(default=False,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
	    return self.name

    @property
    def imageURL(self):
	    try:
		    url = self.image.url
	    except:
		    url = ''
	    return url





# class Customer(models.Model):
# 	student = models.OneToOneField(Student, null=True, blank=True, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=200, null=True)
# 	email = models.CharField(max_length=200)

# 	def __str__(self):
# 		return self.name


# class Product(models.Model):
# 	name = models.CharField(max_length=200)
# 	price = models.FloatField()
# 	digital = models.BooleanField(default=False,null=True, blank=True)
# 	image = models.ImageField(null=True, blank=True)

# 	def __str__(self):
# 		return self.name

# 	@property
# 	def imageURL(self):
# 		try:
# 			url = self.image.url
# 		except:
# 			url = ''
# 		return url

# class Order(models.Model):
# 	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
# 	date_ordered = models.DateTimeField(auto_now_add=True)
# 	complete = models.BooleanField(default=False)
# 	transaction_id = models.CharField(max_length=100, null=True)

# 	def __str__(self):
# 		return str(self.id)
		
# 	@property
# 	def shipping(self):
# 		shipping = False
# 		orderitems = self.orderitem_set.all()
# 		for i in orderitems:
# 			if i.product.digital == False:
# 				shipping = True
# 		return shipping

# 	@property
# 	def get_cart_total(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.get_total for item in orderitems])
# 		return total 

# 	@property
# 	def get_cart_items(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.quantity for item in orderitems])
# 		return total 

# class OrderItem(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
# 	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
# 	quantity = models.IntegerField(default=0, null=True, blank=True)
# 	date_added = models.DateTimeField(auto_now_add=True)

# 	@property
# 	def get_total(self):
# 		total = self.product.price * self.quantity
# 		return total

# class ShippingAddress(models.Model):
# 	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
# 	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
# 	address = models.CharField(max_length=200, null=False)
# 	city = models.CharField(max_length=200, null=False)
# 	state = models.CharField(max_length=200, null=False)
# 	zipcode = models.CharField(max_length=200, null=False)
# 	date_added = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.address