from django.contrib import admin
from django.urls import path, include  # ensure include is imported
from django.conf import settings
from django.conf.urls.static import static
from .views import home, send_email_view, get_template_content


urlpatterns = [
    path('', home, name='home'),
    path('send_email/', send_email_view, name='send_email'),
    path('get_template_content/<int:template_id>/', get_template_content, name='get_template_content'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)