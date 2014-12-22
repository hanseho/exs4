from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Menu(models.Model):
	name = models.CharField('name', max_length=100)
	price = models.IntegerField('price',default=0)
	photo_url = models.CharField('photo_url', max_length=100)
	content = models.TextField('contents', default="")

	def __str__(self):
		return self.name

class Order(models.Model):
	name = models.ForeignKey(Menu)
	phone = models.IntegerField('phone',default=0)
	address = models.CharField(max_length=100)
	quantity = models.IntegerField('quantity',default=0)
	user = models.ForeignKey(User)

	def __str__(self):
		return "%s : %s" % (self.name, self.user)

class Bucketlist(models.Model):
	name = models.ForeignKey(Menu)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.name.name