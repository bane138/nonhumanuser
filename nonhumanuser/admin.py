admin.autodiscover()
flatpages.register()
urlpatterns += [ url(r'^admin/', include(admin.site.urls)), ]