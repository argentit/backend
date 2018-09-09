from django.http import HttpResponse
from django.conf import settings

def robots_txt(request):
	try:
		path = settings.BASE_DIR + '/../robots.txt'
		file = open(path, 'r')
		content = file.read()
		return HttpResponse(content, content_type='text/plain')
	except Exception as e:
		print(e)
		return HttpResponse(content_type='text/plain')
