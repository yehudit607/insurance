from django.test import TestCase
from api.models import Submission, StatusChoices
from api.submissions.dto.submission_dto import SubmissionCreateDto, SubmissionDto, SubmissionUpdateDto
from modules.submission.src.services import SubmissionService


class SubmissionServiceTestCase(TestCase):
    def setUp(self):
        self.service = SubmissionService()

    def test_create_submission(self):
        # Create a new submission record
        submission_data = SubmissionCreateDto(
            broker_id=1,
            company_name='Test Company',
            physical_address='123 Test St',
            annual_revenue=1000000,
            status=StatusChoices.NEW
        )
        submission_dto = self.service.create(submission_data)

        # Verify that the submission was created
        assert isinstance(submission_dto, SubmissionDto)

        # Cleanup: delete the submission record
        self.service.delete(submission_dto.id)

    def test_update_submission(self):
        # Create a new submission record
        submission_data = SubmissionCreateDto(
            broker_id=1,
            company_name='Test Company',
            physical_address='123 Test St',
            annual_revenue=1000000,
            status=StatusChoices.IN_PROGRESS
        )
        submission_dto = self.service.create(submission_data)

        # Update the submission record
        submission_update_data = SubmissionUpdateDto(
            submission_id=submission_dto.id,
            company_name='New Test Company',
            physical_address='456 New St',
            annual_revenue=2000000,
            status=StatusChoices.UPLOADED
        )
        success = self.service.update(submission_update_data)

        # Verify that the submission was updated
        assert success
        submission = Submission.objects.get(id=submission_dto.id)
        assert submission.company_name == submission_update_data.company_name
        assert submission.physical_address == submission_update_data.physical_address
        assert submission.annual_revenue == submission_update_data.annual_revenue
        assert submission.status == submission_update_data.status

        # Cleanup: delete the submission record
        self.service.delete(submission_dto.id)

    def test_delete_submission(self):
        # Create a new submission record
        submission_data = SubmissionCreateDto(
            broker_id=1,
            company_name='Test Company',
            physical_address='123 Test St',
            annual_revenue=1000000,
            status=StatusChoices.NEW
        )
        submission_dto = self.service.create(submission_data)

        # Delete the submission record
        success = self.service.delete(submission_dto.id)

        # Verify that the submission was deleted
        assert success
        with self.assertRaises(Submission.DoesNotExist):
            Submission.objects.get(id=submission_dto.id)

    def test_list_submissions(self):
        # Create some submission records
        submission_data_1 = SubmissionCreateDto(
            broker_id=1,
            company_name='Test Company 1',
            physical_address='123 Test St',
            annual_revenue=1000000,
            status=StatusChoices.NEW
        )
        submission_data_2 = SubmissionCreateDto(
            broker_id=1,
            company_name='Test Company 2',
            physical_address='456 Test St',
            annual_revenue=2000000,
            status=StatusChoices.UPLOADED
        )
        submission_dto_1 = self.service.create(submission_data_1)
        submission_dto_2 = self.service.create(submission_data_2)

        # List the submission records
        submission_dtos = self.service.list(1)

        # Verify that all submission records were returned
        assert isinstance(submission_dtos, list)
