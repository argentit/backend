from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.models import Article
from alfa.forms import *
from alfa.decorators import *


def news_page(request):
	context = {}
	context['all'] = Article.objects.all()
	return render(request, 'news/news_page.html', context)

@has_premission()
def new_news_page(request):
	context = {}
	if request.method == 'POST':
		form = NewsForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.save()
			return HttpResponseRedirect(reverse('news_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.'
	context['form'] = NewsForm()
	context['form'].required_css_class = 'container p-0  rounded-0'
	context['form']['title'].label_classes = ('container-fluid pl-0')
	form_items = []
	return render(request, 'news/new_news_page.html', context)

@has_premission()
def edit_news_page(request, id):
	context = {}
	
	return HttpResponse('ok')

@has_premission()
def remove_news_page(request, id):
	context = {}
	try:
		article = Article.objects.get(id=id)
	except Article.DoesNotExist:
		return HttpResponseRedirect(reverse('news_url'))
	if request.method == 'POST':
		article.delete()
		return HttpResponseRedirect(reverse('news_url'))
	else:
		context['article'] = article
		context['back_url'] = reverse('news_url')
		context['text'] = 'Действительно удалить статью с заголовом \"' + article.title + '\"' + '?'
		return render(request, 'admin/really_remove_page.html', context)
