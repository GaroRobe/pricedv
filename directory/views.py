# Create your views here.
from django.http import HttpResponse
from directory.models import *


def categories(request):
    rootNodes = Node.objects.filter(parent_id = 1)
    t = loader.get_template('frontend/main.html')
    c = Context({
        'rootNodes': rootNodes,
    })
    return HttpResponse(t.render(c))