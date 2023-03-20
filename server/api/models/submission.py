from django.db import models

from api.models.user import UserProfile
from infra.base import Choice


class StatusChoices(Choice):
    NEW = 'NEW'
    UPLOADED = 'UPLOADED'


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    physical_address = models.CharField(max_length=255)
    annual_revenue = models.IntegerField(null=True)
    status = models.TextField(StatusChoices, default=StatusChoices.NEW)
    application_file = models.FileField(upload_to='applications/', null=True, blank=True)
    broker = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='submissions',
        null=True,
    )

    class Meta:
        app_label = "api"

    def __str__(self):
        return self.company_name
