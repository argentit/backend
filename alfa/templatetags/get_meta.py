from django import template
from django.urls import resolve

register = template.Library()
from alfa.models import PageMetaData
from alfa.forms import MetaDataForm

@register.simple_tag
def get_meta(request, *args):
	try:
		return PageMetaData.objects.get(url=request.path)
	except PageMetaData.DoesNotExist:
		if request.user.is_authenticated:
			obj = PageMetaData()
			obj.url = request.path
			obj.save()
		else:
			obj = None
		return obj

@register.simple_tag
def get_meta_form(obj, *args):
	if obj == None:
		return None
	return MetaDataForm(instance=obj)
