from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
	url(r'^select2/', include('django_select2.urls')),
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
	path('', include('alfa.urls')),
	#path('djadmin', admin.site.urls),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
