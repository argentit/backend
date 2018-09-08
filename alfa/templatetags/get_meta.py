from django import template

register = template.Library()
from alfa.models import PageMetaData
from alfa.forms import MetaDataForm

@register.simple_tag
def get_meta(path, *args):
	try:
		return PageMetaData.objects.get(url=path)
	except PageMetaData.DoesNotExist:
		obj = PageMetaData()
		obj.url = path
		obj.save()
		return obj

@register.simple_tag
def get_meta_form(obj, *args):
	return MetaDataForm(instance=obj)
