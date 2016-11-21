from django.http import HttpResponse
from django.shortcuts import render

import diff
import json


def index(request):
    return render(request, 'website_diff/index.html')
    return HttpResponse("Hello, world. You're at the polls index.")


def check_for_changes(request):
    diff.run()
    return HttpResponse("Checked for changes!")


def get_domains(request):
    data = map(lambda x: x.keys()[0], diff.get_data())
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_diff(request):
    f1 = 'data/store_data/webversioning.github.io/webversioning.github.io/webversioning.github.io*2016-11-21 19:35:10.490732'
    f2 = 'data/store_data/webversioning.github.io/webversioning.github.io/webversioning.github.io*2016-11-21 20:33:19.771246'
    f1 = diff.read_file(f1)
    f2 = diff.read_file(f2)

    res, is_diff = diff.perform_diff(f1, f2)
    
    data = {'original_file': f1.splitlines(),
            'new_file': f2.splitlines(),
            'diff_file': res}
    return HttpResponse(json.dumps(data), content_type='application/json')
