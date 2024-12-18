from django.urls import re_path as url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name='tamilmatrimony'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^profiles/', include('tamilmatrimony.urls', namespace='profiles')),
    url(r'', include('tamilmatrimony.urls', namespace='profiles')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)