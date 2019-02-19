from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path


def root(request):
    # TODO: 차후에 URL Reverse 기능
    return HttpResponseRedirect('/blog/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('bot/', include('bot.urls')),
    path('shop/', include('shop.urls')),
    path('', root),
]
