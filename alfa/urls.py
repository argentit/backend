from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.views.generic import RedirectView

from alfa.views import views, jobs, news, charity, for_patients, info, service, doctors, technologies, comments, results, home, views, about

urlpatterns = [
				url(r'^admin/', include('alfa.admin_urls')),
				url(r'^$', home.home_page, name = 'home_url'),
				url(r'^doctors/$', doctors.doctors_page, name = 'doctors_url'),
				url(r'^doctors/(?P<id>\d+)$', doctors.doctor_page, name = 'doctor_url'),
				url(r'^technologies/$', technologies.technologies_page, name = 'technologies_url'),
				url(r'^technologies/(?P<id>\d+)$', technologies.technology_page, name = 'technology_url'),
				url(r'^services/$', service.services_page, name = 'services_url'),
				url(r'^service/(?P<id>\d+)', service.service_page, name = 'service_url'),
				url(r'^results/$', results.results_page, name='results_url'),
				url(r'^comments/$', comments.comments_page, name='comments_url'),
				url(r'^news/$', news.news_page, name='news_url'),
				url(r'^job/$', jobs.jobs_page, name='jobs_url'),
				url(r'^charity/$', charity.charity_page, name='charity_url'),
				url(r'^for_patients/$', for_patients.for_patients_page, name='for_patients_url'),
				url(r'^for_patients/dms/$', for_patients.dms_page, name='dms_url'),
				url(r'^info/$', info.info_page, name='info_url'),
				url(r'^about/$', about.about_page, name='about_url'),
				url(r'robots.txt', views.robots_txt, name='robots_txt_url'),
				# url(r'', views.return404, name='404_url'),
				]
