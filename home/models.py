from django.db import models

class DevTicket(models.Model):
    user = models.CharField(max_length=255, default='unknown user')
    ticket_id = models.CharField(max_length=255, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DevTicket {self.id}"

class EmailLog(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    to_email = models.EmailField()
    from_email = models.EmailField()
    cc_email = models.EmailField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)