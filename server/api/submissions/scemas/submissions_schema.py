from rest_framework import serializers
from server.modules.submission.src.models.submission import StatusChoices


class SubmissionsSchemas(serializers.Serializer):
    company_name = serializers.CharField(required=True)
    physical_address = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    annual_revenue = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=StatusChoices.values(), required=True)
    application_file = serializers.FileField(required=False)
