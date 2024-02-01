from django.urls import path
from .views import home, send_email_view, get_template_content


urlpatterns = [
    path('', home, name='home'),
    path('send_email/', send_email_view, name='send_email'),
    path('get_template_content/<int:template_id>/', get_template_content, name='get_template_content'),
]
