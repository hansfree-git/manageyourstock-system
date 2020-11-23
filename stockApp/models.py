from django.db import models
from django.utils.text import slugify

class Category(models.Model):
	name=models.CharField(max_length=200, blank=True, null=True, unique=True) #unique = true ensures no duplicate is added
	slug=models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural='Categories'


	def save(self , *args , **kwargs):
		if not self.slug and self.name:
			self.slug = slugify(self.name)
		super(Category , self).save(*args , **kwargs)

class Stock(models.Model):
	category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	item_name=models.CharField(max_length=200, blank=True, null=True)
	slug=models.CharField(max_length=200, blank=True, null=True)
	quantity=models.PositiveIntegerField(default=0)
	receive_quantity=models.PositiveIntegerField(default=0)
	receive_by=models.CharField(max_length=50, blank=True, null=True)
	issue_quantity=models.PositiveIntegerField(default=0)
	issue_by=models.CharField(max_length=50, blank=True, null=True)
	issue_to=models.CharField(max_length=50, blank=True, null=True)
	phone_number=models.CharField(max_length=50, blank=True, null=True)
	created_by=models.CharField(max_length=50, blank=True, null=True)
	reorder_level=models.PositiveIntegerField(default=0)
	last_updated=models.DateTimeField(auto_now=True)
	date_created=models.DateTimeField(auto_now_add=False, auto_now=True)


	def __str__(self):
		return self.item_name

	class Meta:
		verbose_name_plural='Stocks'
		ordering=['-last_updated']

	# slugify the name of the new item added through form
	def save(self , *args , **kwargs):
		if not self.slug and self.item_name:
			self.slug = slugify(self.item_name)
		super(Stock , self).save(*args , **kwargs)