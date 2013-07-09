from django.conf.urls import patterns, include, url
urlpatterns = patterns('', url(r'^auth/', include('social_auth.urls')),)
