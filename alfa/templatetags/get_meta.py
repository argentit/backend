from django import template
from django.urls import resolve

register = template.Library()
from alfa.models import PageMetaData
from alfa.forms import MetaDataForm

@register.simple_tag
def get_meta(request, *args):
	try:
		if request.user.is_authenticated:
			return PageMetaData.objects.get(url=request.path)
		else:
			return None
	except PageMetaData.DoesNotExist:
		obj = PageMetaData()
		obj.url = request.path
		obj.save()
		return obj

@register.simple_tag
def get_meta_form(obj, *args):
	if obj == None:
		return None
	return MetaDataForm(instance=obj)
