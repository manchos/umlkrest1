from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rd90 import views
from django.conf.urls import include

urlpatterns = [
    url(r'^rd90/$',  views.Rd90CalcList.as_view()),
    url(r'^rd90/(?P<pk>[0-9]+)/$', views.Rd90CalcDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)