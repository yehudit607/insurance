from django.urls import path
from .submissions.views import submissions


urlpatterns = [
    path("submission", submissions.SubmissionView.as_view()),
    path("submission/<int:submission_id>", submissions.SubmissionView.as_view()),
    path('submission/<int:submission_id>/upload-pdf/', PdfUploadView.as_view(), name='pdf-upload'),


]
