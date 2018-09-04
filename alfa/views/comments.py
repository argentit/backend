from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from alfa.decorators import *
from alfa.models import Portal
from alfa.forms import EditPortalForm


def comments_page(request):
	context = {}
	context['all_portals'] = Portal.objects.all()
	return render(request, 'comments/comments_page.html', context)

@has_premission()
def edit_portal_page(request, id=None):
	context = {}
	template_name = 'comments/edit_portal_page.html'

	try:
		if id is not None:
			portal = Portal.objects.get(id=id)
			context['header'] = 'Изменить портал'
		else:
			portal = None
			context['header'] = 'Добавить портал'
	except Portal.DoesNotExist:
		portal = None
	context['form'] = EditPortalForm(instance=portal)
	try:
		if request.method == 'POST':
			form = EditPortalForm(request.POST, request.FILES, instance=portal)
			context['form'] = form
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('comments_url'))
			else:
				context['error'] = True
				context['error_message'] = 'Произошла ошибка.<br>' + str(form.errors)
				return render(request, template_name, context)
		else:
			return render(request, template_name, context)

	except Exception as e:
		context['error'] = True
		context['error_message'] = 'Произошла ошибка.<br>' + str(e)
		return render(request, template_name, context)

@has_premission()
def remove_portal_page(request, id):
	try:
		portal = Portal.objects.get(id=id)
	except Portal.DoesNotExist:
		return HttpResponseRedirect(reverse('comments_url'))
	portal.delete()
	return HttpResponseRedirect(reverse('comments_url'))
