from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.http import Http404
from django.views import View
from django.shortcuts import render
from alfa.forms import ImageTextForm
from alfa.models import ImageText
from django.urls import reverse


class ImageTextView(View):
	template_name = 'image_text_page.html'

	def get(self, request, type, id=None):
		context = {}
		if id == 0:
			context['header'] = 'Добавить пост'
			obj = None
		else:
			context['header'] = 'Изменить пост'
			try:
				obj = ImageText.objects.get(id=id)
			except:
				obj = None
		context['form'] = ImageTextForm(instance=obj)
		return render(request, self.template_name, context)

	def post(self, request, type, id=0):
		context = {}
		obj = None
		if id != 0:
			try:
				obj = ImageText.objects.get(id=id)
			except:
				obj = None
		form = ImageTextForm(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.type = 'home'
			obj.save()
			return HttpResponseRedirect(reverse('home_url'))
		else:
			context['error'] = True
			context['error_message'] = 'Неверно заполнена форма.' + str(form.errors)
			context['form'] = ImageTextForm(instance=obj)
			return render(request, self.template_name, context)

def remove_image_text(request, id):
	try:
		obj = ImageText.objects.get(id=id)
		obj.delete()
		return HttpResponseRedirect(reverse('home_url'))
	except:
		return HttpResponseRedirect(reverse('home_url'))
