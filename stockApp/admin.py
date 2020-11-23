from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from.models import Category, Stock
from django import forms

# creating a customized form from the stock modelform
class AdminStockCreateForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['category','item_name','slug','quantity', 'reorder_level']

class StockAdmin(ImportExportModelAdmin):
	# sets values for how the admin site lists your products
    list_display = ('item_name', 'category', 'quantity', 'date_created', 'last_updated',)
    # which of the fields in 'list_display' tuple link to admin product page
    list_display_links = ('item_name',)
    list_per_page = 50
    ordering = ['-date_created']
    search_fields = ['category','item_name']
    exclude = ('date_created', 'last_updated',)
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug': ('item_name',)}
    form=AdminStockCreateForm
admin.site.register(Stock,StockAdmin)


class CategoryAdmin(ImportExportModelAdmin):
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)