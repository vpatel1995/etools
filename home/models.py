from django.db import models

class DevTicket(models.Model):
    user = models.CharField(max_length=255, default='unknown user')
    ticket_id = models.CharField(max_length=255, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DevTicket {self.id}"
