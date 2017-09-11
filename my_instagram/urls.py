from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from my_instagram import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('photo_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
