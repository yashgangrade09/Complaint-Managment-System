from django.conf.urls import patterns, url
from django.conf.urls.static import static
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_complaint/',views.add_complaint,name='add_complaint'),
        url(r'^complaints/',views.view_complaint,name='view complaint'),
        url(r'^login/',views.loginview,name='login'),
        url(r'^logout/',views.logoutview,name='logout'),
        url(r'^edit/',views.editview,name='edit complaint'),
        url(r'^delete/(?P<complaint_id>[0-9]+)/$',views.deleteview,name='delete complaint'),
        url(r'^confirm/',views.confirmview,name='alter complaint'),
                       )
