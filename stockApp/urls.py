from django.urls import path
from.import views

urlpatterns=[
	path('', views.home, name='home-page'), #home-page
	path('catalog-list/', views.catalog_list, name='catalog-list'),
	path('add-item/', views.add_item, name='add-item'),
	path('add-category/',views.add_category, name='add-category'),
	path('<slug:category_slug>/show-category/',views.show_category, name='show-category'),
	path('<slug:product_slug>/update-item/', views.update_item, name='update-item'),
	path('<slug:product_slug>/delete-item/', views.delete_item, name='delete-item'),
	path('<slug:product_slug>/detail/', views.item_detail, name='item-detail'),
	path('<slug:product_slug>/issue/', views.issue_item, name='item-issue'),
	path('<slug:product_slug>/receive/', views.receive_item, name='item-receive'),
	path('<slug:product_slug>/re-order/', views.re_order, name='re-order'),

	path('search-results/', views.results, name='search-results'),
	path('history/', views.history, name='item-history'),
]