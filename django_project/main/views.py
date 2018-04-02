from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.urls import reverse


from .models import *


def index(request):
    latest_documents_list = Document.objects.order_by('-date_of_creation')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))
    # return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, document_id):
    try:
        document = get_object_or_404(Document, pk=document_id)
    except Document.DoesNotExist:
        raise Http404("Document does not exist!")
    return render(request, 'polls/detail.html', {'document': document})


def index_data(request):
    latest_documents_list = Data.objects.order_by('-date_of_creation')[:5]
    template = loader.get_template('polls/index_data.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))
    # return HttpResponse("Hello, world. You're at the polls index.")


# def add_document(request):
#     document = Document
#     try:
#         selected_choice = document(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'document': document,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(document.id,)))



# def detail(request, document_id):
#     return HttpResponse("You're looking at question %s." % document_id)


def results(request, document_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % document_id)


def vote(request, document_id):
    return HttpResponse("You're voting on question %s." % document_id)
