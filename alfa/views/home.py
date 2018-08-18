from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import HomePost, CarouselElement
from alfa.forms import HomePostForm, CarouselElementForm
from alfa.decorators import *

def home_page(request):
	context = {}
	template_name = 'home/home_page.html'
	context['all_posts'] = HomePost.objects.all()
	all = CarouselElement.objects.all()
	print(all)
	if all.count() == 0:
		return render(request, template_name, context)
	context['active_element'] = all[0]
	context['carousel'] = all[1:]
	return render(request, template_name, context)

@has_premission()
def new_home_page(request):
	context = {}
	template_name = 'home/new_home_page.html'
	if request.method == 'POST':
		form = HomePostForm(request.POST)
		if form.is_valid():
			post = HomePost()
			post.text = form.cleaned_data['text']
			post.title = form.cleaned_data['title']
			post.url = form.cleaned_data['url']
			post.save()
			return HttpResponseRedirect(reverse('home_url'))
		else:
			context['error'] = True
			context['form'] = HomePostForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = HomePostForm()
		return render(request, template_name, context)

@has_premission()
def remove_home_post_page(request, id):
	context = {}
	try:
		post = HomePost.objects.get(id=id)
	except HomePost.DoesNotExist:
		return HttpResponseRedirect(reverse('home_url'))
	if request.method == 'POST':
		post.delete()
		return HttpResponseRedirect(reverse('home_url'))
	else:
		context['back_url'] = reverse('home_url')
		context['text'] = 'Действительно удалить пост \"' + str(post) + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)

@has_premission()
def new_carousel_element_page(request):
	context = {}
	template_name = 'home/new_carousel_element_page.html'
	if request.method == 'POST':
		form = CarouselElementForm(request.POST, request.FILES)
		if form.is_valid():
			element = CarouselElement()
			element.title = form.cleaned_data['title']
			element.text = form.cleaned_data['text']
			element.image = form.cleaned_data['image']
			element.post = form.cleaned_data['post']
			element.save()
			element.number = str(element.id)
			element.save()
			return HttpResponseRedirect(reverse('home_url'))
		else:
			context['error'] = True
			context['form'] = CarouselElementForm()
			context['error_message'] = 'Неверно заполнена форма.'
			return render(request, template_name, context)
	else:
		context['form'] = CarouselElementForm()
		return render(request, template_name, context)

@has_premission()
def edit_carousel_page(request):
	context = {}
	template_name = 'home/carousel_elements_page.html'
	context['carousel'] = CarouselElement.objects.all()
	return render(request, template_name, context)

@has_premission()
def carousel_element_move_up_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('edit_carousel_url'))
	items = CarouselElement.objects.filter(number__lte=item.number).order_by('-number')
	if items.count() > 1:
		one = items[0]
		two = items[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('edit_carousel_url'))

@has_premission()
def carousel_element_move_down_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('edit_carousel_url'))
	items = CarouselElement.objects.filter(number__gte=item.number).order_by('-number')
	if items.count() > 1:
		one = items[0]
		two = items[1]
		tmp = one.number
		one.number = two.number
		two.number = tmp
		one.save()
		two.save()
	return HttpResponseRedirect(reverse('edit_carousel_url'))

@has_premission()
def remove_carousel_element_page(request, id):
	try:
		item = CarouselElement.objects.get(id=id)
	except CarouselElement.DoesNotExist:
		return HttpResponseRedirect(reverse('edit_carousel_url'))
	item.delete()
	return HttpResponseRedirect(reverse('edit_carousel_url'))
