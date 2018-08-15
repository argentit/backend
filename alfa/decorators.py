from django.http import HttpResponseRedirect

def has_premission():
	def has(f):
		def func(request, *args, **kwargs):
			if request.user.is_superuser:
				return f(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(reverse('main_url'))
		return func
	return has
