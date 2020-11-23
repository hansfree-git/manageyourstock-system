from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Stock
from.forms import *

import pytz
from django.utils import timezone
from datetime import datetime
import csv
# Create your views here.

def home(request, template_name='stockApp/index.html'):
	try:
		total_category=Category.objects.all().count()
		total_stock=Stock.objects.all().count()

		stock=Stock.objects.all()
		total_q=[]
		re_order=[]

		for item in stock:
			total_q.append(item.quantity)
			total_quantity=sum(total_q)

			if item.quantity<=item.reorder_level:
				re_order.append(item)
				reorder_items=len(re_order)
	except:
		pass

	return render(request, template_name, locals())

@login_required
def catalog_list(request, template_name='stockApp/catalog_list.html'):
	stock_list=Stock.objects.all().order_by('-last_updated')

	paginator = Paginator(stock_list, 4)
	page = request.GET.get('page')
	stock_list = paginator.get_page(page)
	try:
		page_objects = paginator.page(page)
	except PageNotAnInteger:
		page_objects = paginator.page(1)
	except EmptyPage:
		page_objects = paginator.page(paginator.num_pages)

	return render(request, template_name, locals())

@login_required
def add_item(request, template_name='stockApp/add_item.html'):
	# StockFormset=formset_factory(StockCreateForm,extra=5, can_delete=True)
	form=StockCreateForm()
	if request.method=='POST':
		form=StockCreateForm(request.POST or None)
		if form.is_valid():
			category=form.cleaned_data.get('category')
			item_name=form.cleaned_data.get('item_name')
			quantity=form.cleaned_data.get('quantity')
			form.save(commit=False)
			# checking if item already exists
			for instance in Stock.objects.all():
				if item_name==instance.item_name:
					messages.error(request,'%s already exists, consider updating'%instance.item_name)
				else:
					# else if item doesn't exists, gp ahead and add to database
					form.save()
					messages.success(request,'%s is successfuly added'%instance.item_name)
			
			return HttpResponseRedirect(reverse('catalog-list'))
		
	return render(request, template_name, locals())

@login_required
def add_category(request, template_name='stockApp/add_category.html'):
	form=StockCategoryForm()
	if request.method=='POST':
		form=StockCategoryForm(request.POST or None)
		if form.is_valid():
			# category_name=form.cleaned_data['name']
			# form.save(commit=False)
			# try:
			# 	instance=Category.objects.get(name=category_name)
			# 	if instance == category_name:
			# 		print(instance)
			# 		messages.error(request,'{} category already exists, try adding products'.format(instance))
			# 		return redirect('add-category')
			# except Category.DoesNotExist:
			form.save()
			return redirect('add-item')
	return render(request, template_name, locals())

@login_required
def update_item(request,product_slug,template_name='stockApp/update_item.html'):
	item=get_object_or_404(Stock,slug=product_slug)
	form=StockUpdateForm(instance=item)
	if request.method=='POST':
		form=StockUpdateForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('catalog-list'))

	return render(request, template_name, locals())

@login_required
def delete_item(request,product_slug,template_name='stockApp/delete_item.html'):
	item=get_object_or_404(Stock,slug=product_slug)
	if request.method=='POST':
		item.delete()
		messages.success(request,'%s successfuly deleted'%item.item_name)
		return HttpResponseRedirect(reverse('catalog-list'))
	return render(request, template_name, locals())

@login_required
def item_detail(request,product_slug,template_name='stockApp/detail_item.html'):
	item=get_object_or_404(Stock,slug=product_slug)


	return render(request, template_name, locals())
@login_required
def issue_item(request,product_slug,template_name='stockApp/issue_item.html'):
	item=get_object_or_404(Stock,slug=product_slug)
	form =IssueForm()
	if request.method=='POST':
		form=IssueForm(request.POST or None, instance=item)
		if form.is_valid():
			quantity=form.cleaned_data['issue_quantity']
			item.quantity-=quantity
			item.issue_to=form.cleaned_data['issue_to']
			form.save()
			item.issue_by=str(request.user)
			messages.success(request,'{} {} successfully issued to {}'.format(quantity,item.item_name,item.issue_to))
			return HttpResponseRedirect(reverse('item-detail', args=(item.slug,)))
	return render(request, template_name, locals())


@login_required
def receive_item(request,product_slug,template_name='stockApp/receive_item.html'):
	item=get_object_or_404(Stock,slug=product_slug)
	form =ReceiveForm()
	if request.method=='POST':
		form=ReceiveForm(request.POST or None, instance=item)
		if form.is_valid():
			quantity=form.cleaned_data['receive_quantity']
			item.quantity+=quantity
			item.receive_by=form.cleaned_data['receive_by']
			form.save()
			messages.success(request,'{} {} successfully received from {}'.format(quantity,item.item_name,item.receive_by))
			return HttpResponseRedirect(reverse('item-detail', args=(item.slug,)))
	return render(request, template_name, locals())

@login_required
def re_order(request,product_slug,template_name='stockApp/re_order.html'):
	item=get_object_or_404(Stock,slug=product_slug)
	form=ReorderForm()
	if request.method=='POST':
		form=ReorderForm(request.POST or None, instance=item)
		if form.is_valid():
			instance=form.save(commit=False)
			messages.success(request,'Re-order level for {} updated to {}'.format(item.item_name, instance.reorder_level))
			instance.save()
			return redirect('catalog-list')
	return render(request, template_name, locals())
@login_required
def show_category(request, category_slug, template_name='stockApp/show_category.html'):
	try:
		category=get_object_or_404(Category, slug=category_slug)
		stock_list=category.stock_set.all()

		paginator = Paginator(stock_list, 4)
		page = request.GET.get('page')
		stock_list = paginator.get_page(page)
	except:
		pass
	try:
		page_objects = paginator.page(page)
	except PageNotAnInteger:
		page_objects = paginator.page(1)
	except EmptyPage:
		page_objects = paginator.page(paginator.num_pages)
	return render(request, template_name, locals())


@login_required
def results(request, template_name='tags/result_page.html'):
	stock_list=Stock.objects.all()
	if request.method=='POST':
		search_form=StockSearchForm(request.POST or None)
		start_date=request.POST.get('start_date')
		end_date=request.POST.get('end_date')

		# convert string to datetime
		# start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
		# end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

		# # convert dates to timezones
		# timezone=pytz.timezone('America/New_York')
		# timezone_start_date_obj=timezone.localize(start_date_obj)
		# timezone_end_date_obj=timezone.localize(end_date_obj)

		# print(timezone_start_date_obj)
		# print(timezone_end_date_obj)

		stock_list=Stock.objects.filter(
			Q(category__name__icontains= search_form['item_name'].value())|
			Q(item_name__icontains=search_form['item_name'].value())
			# Q(last_updated__gte=start_date) & Q(last_updated__lte=end_date)
			)

		if search_form['export_to_csv'].value()==True:
			response = HttpResponse(content_type = 'text/csv')
			response['Content-Disposition'] = 'attachment; filename = "list of stock.csv" ' 

			writer = csv.writer(response)
			writer.writerow(['PRODUCT','CATEGORY','QUANTITY'])
			
			for i in stock_list:
				writer.writerow([i.item_name,i.category,i.quantity])
			return response

	paginator = Paginator(stock_list, 4)
	page = request.GET.get('page')
	stock_list = paginator.get_page(page)
	try:
		page_objects = paginator.page(page)
	except PageNotAnInteger:
		page_objects = paginator.page(1)
	except EmptyPage:
		page_objects = paginator.page(paginator.num_pages)

	return render(request, template_name, locals())


@login_required
def history(request, template_name='stockApp/history_list.html'):
	stock_list=Stock.objects.all()

	paginator = Paginator(stock_list, 4)
	page = request.GET.get('page')
	stock_list = paginator.get_page(page)
	try:
		page_objects = paginator.page(page)
	except PageNotAnInteger:
		page_objects = paginator.page(1)
	except EmptyPage:
		page_objects = paginator.page(paginator.num_pages)

	return render(request, template_name, locals())