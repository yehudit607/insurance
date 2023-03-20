from typing import Optional
from api.models.submission import Submission
from infra.base import MISSING, dto_with_optional, ModelToDtoMixin


@dto_with_optional
class SubmissionDto(ModelToDtoMixin):
    id: int
    company_name: str
    physical_address: str
    annual_revenue: float
    status: str
    application_file: Optional[str]
    broker_id: int

    @classmethod
    def from_record(cls, record: Submission):
        return SubmissionDto(
            id=record.submission_id,
            company_name=record.company_name,
            physical_address=record.physical_address,
            annual_revenue=float(record.annual_revenue),
            status=record.status,
            application_file=record.application_file.url if record.application_file else None,
            broker_id=record.broker_id,
        )


@dto_with_optional
class SubmissionCreateDto:
    company_name: str
    physical_address: str
    annual_revenue: float
    status: str
    broker_id: int


@dto_with_optional
class SubmissionUpdateDto:
    submission_id: int
    company_name: Optional[str] = MISSING
    physical_address: Optional[str] = MISSING
    annual_revenue: Optional[int] = MISSING
    status: Optional[str] = MISSING
    broker_id: Optional[int] = MISSING

