from django.http import HttpResponse

from diff import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def check_for_changes(request):
    run()
    return HttpResponse("Checked for changes!")
