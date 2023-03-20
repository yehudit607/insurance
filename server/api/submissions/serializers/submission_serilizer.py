from rest_framework_dataclasses.serializers import DataclassSerializer

from api.submissions.dto.submission_dto import SubmissionDto


class SubmissionSerializer(DataclassSerializer):
    class Meta:
        dataclass = SubmissionDto
        fields = "__all__"
