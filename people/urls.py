from django.conf.urls import url, include

from people import views


urlpatterns = [
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^hackerrank/$', views.HackerRankView.as_view(), name='hackerrank'),
    url(r'^dataweave/$', views.DataWeaveView.as_view(), name='dataweave'),
    url(r'^$', views.Dashboard.as_view(), name='dashboard'),
]
