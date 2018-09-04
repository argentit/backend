from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import CarouselElement, Text
from alfa.forms import  NewCarouselElementForm, EditCarouselElementForm
from alfa.decorators import *

def about_page(request):
	context = {}
	template_name = 'about/about_page.html'
	try:
		context['text'] = Text.objects.get(name='about')
	except Text.DoesNotExist:
		context['text'] = None
	all = CarouselElement.objects.filter(location='about',)
	if all.count() == 0:
		return render(request, template_name, context)
	context['active_element'] = all[0]
	context['carousel'] = all[1:]
	return render(request, template_name, context)

@has_premission()
def new_carousel_element_page(request):
	context = {}
	template_name = 'about/new_carousel_element_page.html'
	try:
		if request.method == 'POST':
			form = NewCarouselElementForm(request.POST, request.FILES)
			if form.is_valid():
				element = form.save(commit=False)
				element.location = 'about'
				element.save()
				return HttpResponseRedirect(reverse('about_edit_carousel_element_url', kwargs={'id': element.id}))
			else:
				context['error'] = True
				context['form'] = NewCarouselElementForm()
				context['error_message'] = 'Неверно заполнена форма.'
				return render(request, template_name, context)
		else:
			context['form'] = NewCarouselElementForm()
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = NewCarouselElementForm()
		return render(request, template_name, context)

@has_premission()
def edit_carousel_element_page(request, id):
	context = {}
	template_name = 'about/new_carousel_element_page.html'
	try:
		element = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('about_url'))
	try:
		if request.method == 'POST':
			form = EditCarouselElementForm(request.POST, request.FILES, instance=element)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('about_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Произошла ошибка.<br>' + str(form.error)
				context['form'] = form
				return render(request, template_name, context)
		else:
			context['form'] = EditCarouselElementForm(instance=element)
			return render(request, template_name, context)
	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		context['form'] = EditCarouselElementForm(instance=element)
		return render(request, template_name, context)

@has_premission()
def edit_carousel_page(request):
	context = {}
	template_name = 'about/carousel_elements_page.html'
	context['carousel'] = CarouselElement.objects.filter(location='about')
	return render(request, template_name, context)

@has_premission()
def carousel_element_move_up_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('about_edit_carousel_url'))
	items = CarouselElement.objects.filter(location='about', number__lte=item.number).order_by('-number')
	if items.count() > 1:
		one = items[0]
		two = items[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('about_edit_carousel_url'))

@has_premission()
def carousel_element_move_down_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('about_edit_carousel_url'))
	items = CarouselElement.objects.filter(location='about', number__gte=item.number).order_by('-number')
	if items.count() > 1:
		one = items[0]
		two = items[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('about_edit_carousel_url'))

@has_premission()
def remove_carousel_element_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('about_edit_carousel_url'))
	item.delete()
	return HttpResponseRedirect(reverse('about_edit_carousel_url'))
