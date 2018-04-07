from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.urls import reverse


from .models import *


def index(request):
    # pass
    latest_documents_list = Document.objects.order_by('-date_of_creation')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))
    # return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, id):
    try:
        data = get_object_or_404(Data, pk=id)
    except Data.DoesNotExist:
        raise Http404("Document does not exist!")
    return render(request, 'polls/detail.html', {'data': data})


def detail2(request, document_id):
    try:
        document = get_object_or_404(Document, pk=document_id)
    except Document.DoesNotExist:
        raise Http404("Document does not exist!")
    return render(request, 'polls/detail.html', {'document': document})


def index_data(request):
    latest_documents_list = Data.objects.order_by('PID')
    template = loader.get_template('polls/index_data.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))
    # return HttpResponse("Hello, world. You're at the polls index.")


def results(request, ID):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % id)


def vote(request, document_id):
    return HttpResponse("You're voting on question %s." % document_id)
