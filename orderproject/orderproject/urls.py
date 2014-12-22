from django.conf.urls import patterns, include, url
from django.contrib import admin
from order.views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'orderproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^(?P<menu_id>\d+)/detail/$', detail),
    url(r'^(?P<menu_id>\d+)/buy/$', buy),
    url(r'^(?P<menu_id>\d+)/buy/submit/$', buy_submit),
    url(r'^signup/$', signup),
    url(r'^logout/$', user_logout),
    url(r'^mypage/$', mypage),
    url(r'^submit_bucketlist/$', submit_bucketlist),
    url(r'^submit_pay/$', submit_pay),
    url(r'^(?P<menu_id>\d+)/add_bucketlist/$', add_bucketlist),
    url(
            r'^login/$',
            'django.contrib.auth.views.login',
            {'template_name': 'login.html'},
            name='login'
        )
)
