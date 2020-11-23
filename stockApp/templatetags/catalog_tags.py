from django import template
from stockApp.models import Category, Stock
from stockApp.forms import StockSearchForm

register = template.Library()

@register.inclusion_tag("tags/category_list.html")
def category_list():
	category = Category.objects.all()
	return {'category': category,}


@register.inclusion_tag("tags/footer.html")
def footer_links():
	return{'home':'Home','contact':'Contact','client':'Clients'}


@register.inclusion_tag("tags/search.html")
def search_box():
	search_form=StockSearchForm()
	
	return {'search_form':search_form}


