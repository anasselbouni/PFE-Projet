from django.contrib import admin
from django.urls import include,  path,re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('LinkedinApp.urls')),
    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)