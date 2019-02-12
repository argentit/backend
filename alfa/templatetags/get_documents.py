from django import template
from alfa.models import Document

register = template.Library()

@register.simple_tag
def get_documents(type=None, *args):
	return Document.objects.filter(type=type).all()
