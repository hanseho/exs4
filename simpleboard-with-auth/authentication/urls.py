from django.conf.urls import patterns, include, url
from django.contrib import admin
from newboard.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authentication.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    # url(r'^board/new/$', new_board),
    url(r'^board/submit/$', submit_board),
    url(r'^board/(?P<board_id>\d+)/$', board),
    url(r'^board/(?P<board_id>\d+)/search/$', board_search),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/$', article),
    url(r'^board/(?P<board_id>\d+)/new/$', new_article),
    url(r'^board/(?P<board_id>\d+)/submit/$', submit_article),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/delete/$', delete_article),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/reply/$', new_reply),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/reply/(?P<reply_id>\d+)/delete/$', delete_reply),
    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name' : 'login.html'}, name='login'),
    url(r'^board/signup/$', signup),
    url(r'^board/signup/submit/$', signup_submit),
    url(r'^logout/$', user_logout),
)
