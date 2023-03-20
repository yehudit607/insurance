import logging
import traceback
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.response import Response


class SubmissionException(ValueError):
    status_code: int
    message: str

    def __init__(self, message=None, status_code=None, *args):
        self.message = message
        self.status_code = status_code
        super(SubmissionException, self).__init__(*args)


def submission_exception(ex):
    return JsonResponse(
        {"Message": ex.message, "Status": ex.status_code},
        status=ex.status_code,
        safe=False,
    )


def general_exception():
    logger.error("general Exception, exception is:")
    traceback.print_exc()
    return Response(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def get_session_logger():
    return logging.getLogger("sayata_logger")


def is_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)

        return JsonResponse({"error": "wrong credentials"}, status=403)

    return wrapper


logger = get_session_logger()
