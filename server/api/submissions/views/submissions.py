from collections import OrderedDict
from http import HTTPStatus
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.views import APIView

from api.submissions.dto.submission_dto import SubmissionCreateDto, SubmissionUpdateDto
from api.submissions.serializers.submission_serilizer import SubmissionSerializer
from infra.helpers import general_exception
from infra.pagination import SayataPaginator
from modules.submission.src.services import SubmissionService


class SubmissionPaginator(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("current_page", self.page.number),
                    ("params", self.request.query_params),
                    ("results", data),
                ]
            )
        )

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.get_full_path()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.get_full_path()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)


class SubmissionView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    pagination_class = SubmissionPaginator
    serializer_class = SubmissionSerializer

    def paginate_queryset(self, queryset):
        self.pagination_class = SubmissionPaginator
        get_all = self.request.query_params.get(
            "basic", False
        ) or self.request.query_params.get("get_all", False)
        if get_all:
            self.pagination_class.page_size = 40000
        return super().paginate_queryset(queryset)

    def response(self, data, status_code=HTTPStatus.OK):
        return JsonResponse(data, safe=False, status=status_code)

    def get(self, request, submission_id=None, **kwargs):
        try:
            if submission_id:
                submission = SubmissionService.get(submission_id, request.user.id)
                if submission:
                    return self.response(SubmissionSerializer(submission).data)
            else:
                submissions = SubmissionService.list(request.user.id)
                return self.response(SubmissionSerializer(submissions, many=True).data)
        except Exception as ex:
            return general_exception()

        return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)

    def create(self, request, *args, **kwarg):
        try:
            submission_create_dto = SubmissionCreateDto(broker_id=request.user.id, **request.data)
            print(submission_create_dto)
            submission = SubmissionService.create(submission_create_dto)
            return self.response(SubmissionSerializer(submission).data, HTTPStatus.CREATED)
        except Exception as ex:
            return general_exception()

    def update(self, request, *args, **kwargs):
        try:
            submission_id = kwargs["submission_id"]
            submission_update_dto = SubmissionUpdateDto(submission_id, **request.data)
            if SubmissionService.update(submission_update_dto):
                return self.response({"success": "Updated successfully"})
        except Exception as ex:
            return general_exception()

        return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            submission_id = kwargs["submission_id"]
            if SubmissionService.delete(submission_id):
                return self.response({"success": "Deleted successfully"}, HTTPStatus.NO_CONTENT)
        except Exception as ex:
            return general_exception()

        return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)


class PdfUploadView(APIView):
    def post(self, request, format=None):
        file_obj = request.FILES['file']
        submission_id = request.data.get('submission_id')

        service = SubmissionService()
        success = service.upload_pdf(file_obj, submission_id)

        if success:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
