from django.http import JsonResponse
from django.utils import timezone


def ping(request):
    return JsonResponse({
        "status": "ok",
        "message": "Django 6 backend raggiunto",
        "timestamp": timezone.now().isoformat(),
    })
