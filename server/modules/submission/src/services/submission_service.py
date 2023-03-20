import os
from typing import List

from django.core.exceptions import ObjectDoesNotExist

from api.models import Submission
from api.models.submission import StatusChoices
from api.submissions.dto.submission_dto import SubmissionDto, SubmissionUpdateDto, SubmissionCreateDto
from webapp import settings


class SubmissionService:
    supported_query_fields = ["id", "user_id"]
    model = Submission
    dto = SubmissionDto

    @classmethod
    def create(cls, request: SubmissionCreateDto) -> SubmissionDto:
        submission_record = Submission.objects.create(
            broker_id=request.broker_id,
            company_name=request.company_name,
            physical_address=request.physical_address,
            annual_revenue=request.annual_revenue,
            status=request.status,
        )

        submission_dto = SubmissionDto.from_record(submission_record)
        return submission_dto

    @classmethod
    def update(cls, request: SubmissionUpdateDto) -> bool:
        submission_id = request.submission_id
        record = cls.model.objects.get(submission_id=submission_id)
        record.company_name = request.company_name
        record.physical_address = request.physical_address
        record.annual_revenue = request.annual_revenue
        record.status = request.status
        record.save()

        return True

    @classmethod
    def delete(cls, id: int) -> bool:
        submission_record = cls.model.objects.filter(id=id)
        deleted = submission_record.delete()

        return True if deleted else False

    @classmethod
    def list(cls, broker_id: int) -> List[SubmissionDto]:
        submissions = Submission.objects.filter(broker_id=broker_id)
        submission_dtos = []

        for submission in submissions:
            submission_dtos.append(SubmissionDto.from_record(submission))

        return submission_dtos

    @classmethod
    def get(cls, submission_id: int, broker_id: int) -> SubmissionDto:
        try:
            submission = Submission.objects.get(submission_id=submission_id, broker_id=broker_id)
            return SubmissionDto.from_record(submission)
        except ObjectDoesNotExist:
            return None

    def upload_pdf(self, file_obj, submission_id):
        file_name = file_obj.name
        # s3_key = f"pdfs/{file_name}"
        #
        # # Upload file to S3
        # s3 = boto3.client('s3',
        #                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        #                   region_name=settings.AWS_S3_REGION_NAME)
        #
        # bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        #
        # try:
        #     s3.upload_fileobj(file_obj, bucket_name, s3_key)
        # except Exception as e:
        #     print(e)
        #     return False

        # Save file locally
        local_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', file_name)

        with open(local_path, 'wb') as f:
            f.write(file_obj.read())

        # Update submission status to UPLOADED
        submission = Submission.objects.get(id=submission_id)
        submission.status = StatusChoices.UPLOADED
        submission.save()

        return True
