from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.http import Http404
from alfa.models import Sale
from alfa.forms import SaleForm

def sales_page(request):
	context = {}
	template_name = 'sales/sales_page.html'
	try:
		if request.method == 'POST':
			pass
		else:
			context['sales'] = Sale.objects.all()
		return render(request, template_name, context)
	except Exception as e:
		print(e)
		return HttpResponse(e, content_type='text/plain')

def sale_page(request, id):
	context = {}
	template_name = 'sales/sale_page.html'
	try:
		context['sale'] = Sale.objects.get(id=id)
		return render(request, template_name, context)
	except:
		return HttpResponseRedirect(reverse('sales_url'))

def new_sale_page(request, id=None):
	context = {}
	template_name = 'sales/new_sale_page.html'
	try:
		sale = Sale.objects.get(id=id)
	except:
		sale = None
	try:
		if request.method == 'POST':
			form = SaleForm(request.POST, request.FILES, instance=sale)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('sales_url'))
		else:
			context['title'] = 'Новая акция'
			context['form'] = SaleForm(instance=sale)
			context['sales'] = Sale.objects.all()
		return render(request, template_name, context)
	except Exception as e:
		print(e)
		return HttpResponse(e, content_type='text/plain')

def remove_sale_page(request, id):
	try:
		obj = Sale.objects.get(id=id)
		obj.delete()
		return HttpResponseRedirect(reverse('sales_url'))
	except:
		return HttpResponseRedirect(reverse('sales_url'))
