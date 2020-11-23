from .models import Category, Stock
from django import forms
from django.conf import settings
import datetime

class StockCreateForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['category','item_name','quantity']

class StockCategoryForm(forms.ModelForm):
	class Meta:
		model=Category
		fields=['name']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['category','item_name','quantity']

class SearchStockForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['category','item_name']


class IssueForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['issue_quantity','issue_to']

class ReceiveForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['receive_quantity','receive_by']

class ReorderForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['reorder_level']


class StockSearchForm(forms.ModelForm):

	item_name=forms.CharField(
		label='',max_length=200, 
		widget=forms.TextInput(attrs={'placeholder':'Search for item'}), 
		required=False
	)
	
	# start_date = forms.DateField(
	# 	widget=forms.widgets.DateInput(format=("%Y-%m-%d"),attrs={'type': 'date'}),
	# 	required=False
	# )
	# end_date = forms.DateField(
		
	# 	widget=forms.widgets.DateInput(format=("%Y-%m-%d"),attrs={'type': 'date',}),
	# 	required=False
	# )

	# start_date=forms.DateTimeField(required=False)
	# end_date=forms.DateTimeField(required=False)
	export_to_csv=forms.BooleanField(required=False)


	class Meta:
		model=Stock
		fields=['item_name']