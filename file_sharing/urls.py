from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('file_sharing.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^folder/(?P<folder>\d+)/$', 'home', name='home'),
    url(r'^upload', 'upload', name='upload'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
