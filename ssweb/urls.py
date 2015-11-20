from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from app.views import UserSignonView, UserConsoleView, UserProfileView
from app.views import PackageUpgradeView, PackageListView
from app.views import UserVPNPasswdChangeView

# For reference only
from django.contrib.auth import urls
# from django.contrib.auth.views import password_change

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ssweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', UserConsoleView.as_view(), name='home'),

    # User related url
    url(r'^user/signon/$', UserSignonView.as_view(), name='user-signon'),
    url(r'^user/console/$', UserConsoleView.as_view(), name='user-console'),
    url(r'^user/nodes/$', UserConsoleView.as_view(), name='user-nodes'),
    url(r'^user/profile/$', UserProfileView.as_view(), name='user-profile'),
    url(r'^user/upgrade/$', PackageUpgradeView.as_view(), name='user-upgrade'),
    url(r'^user/change-vpn-passwd/(?P<pk>\d+)/$',
        UserVPNPasswdChangeView.as_view(), name='user-sspwd-change'),

    url(r'^pricing/$', PackageListView.as_view(), name='pricing'),
)

# Auth url patterns
urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect':'user-profile',
         'template_name':'user/profile.html'}, name='password_change'
    ),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm_uidb36'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
)


if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/images/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
