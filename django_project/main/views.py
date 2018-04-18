from django.db.models import Max

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from main.serializers import DataSerializer

import json
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views import View

from main.models import *

from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.fields.jsonb import KeyTextTransform

@csrf_exempt
@api_view(['POST'])
def create(request):
    data = JSONParser().parse(request)
    serializer = DataSerializer(data=data)  # конструктор с именоваными параметр
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def get_last_id(request):
    last_id = Data.objects.all().aggregate(Max('id'))
    return JsonResponse(last_id, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def test_search(request):
    SW = 'text'
    res = Data.objects.filter(typedoc__search=SW)
    return HttpResponse(res, status=status.HTTP_200_OK)

def index(request):
    # pass
    latest_documents_list = Document.objects.order_by('-date_of_creation')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))


def detail(request, id):
    try:
        data = get_object_or_404(Data, pk=id)
    except Data.DoesNotExist:
        raise Http404("Document does not exist!")
    return render(request, 'polls/detail.html', {'data': data})


# def detail2(request, document_id):
#     try:
#         document = get_object_or_404(Document, pk=document_id)
#     except Document.DoesNotExist:
#         raise Http404("Document does not exist!")
#     return render(request, 'polls/detail.html', {'document': document})


def index_data(request):
    latest_documents_list = Data.objects.order_by('PID')
    template = loader.get_template('polls/index_data.html')
    context = {
        'latest_documents_list': latest_documents_list
    }
    return HttpResponse(template.render(context))
    # return HttpResponse("Hello, world. You're at the polls index.")


# def results(request, ID):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % id)


# def vote(request, document_id):
#     return HttpResponse("You're voting on question %s." % document_id)


@method_decorator(csrf_exempt, name='dispatch')
class MyView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'UID': 0})

    def post(self, request):
        # print('Raw Data: "%s"' % request.body)
        new_emails = json.loads(request.body.decode())
        for new_email in new_emails:
            # print(new_email)
            print("\n\tI've got the email with the following subject:\n\n\t\t{}\n"
                  .format(new_email['metadata']["Subject"].upper()))
            if new_email['attachments']:
                print('\t\tAttachments:\n')
                for attachment in new_email['attachments']:
                    print('\t\t\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'
                          .format(attachment['filename'],
                                  len(attachment['body']),
                                  attachment['MIME']))
        return HttpResponse("OK")

