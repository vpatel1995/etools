from django.urls import path
from .views import home, send_email_view  # Import send_email_view

urlpatterns = [
    path('', home, name='home'),
    path('send_email/', send_email_view, name='send_email'),  # Use send_email_view here
]
