from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', include('index.urls')),
	url(r'^login/',include('login.urls')),
	url(r'^about/',include('about.urls')),
	url(r'^developers/',include('developers.urls')),
	url(r'^signup/',include('signup.urls')),
	url(r'^signin/',include('signin.urls')),
	url(r'^profilepage/',include('profilepage.urls')),
	url(r'^bill/',include('bill.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

