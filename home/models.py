from django.db import models

class DevTable(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'dev_table