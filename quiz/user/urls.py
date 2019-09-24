from django.conf.urls import url
from .views import register_view, account_view, login_view, index, logout_view, user_info
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^register/$', register_view, name='register'),
                  url(r'^account/$', account_view, name='account'),
                  url(r'^login/$', login_view, name='login'),
                  url(r'^logout/$', logout_view, name='logout'),
                  url(r'^user/$', user_info, name='user'),
                  path('', include('social_django.urls')),
                  url(r'^accounts/profile/$', index),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
