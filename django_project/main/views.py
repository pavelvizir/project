import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.urls import reverse
from django.views import View


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


    # def save_events_json(request):
    #     if request.is_ajax():
    #         if request.method == 'POST':
    #             print
    #             'Raw Data: "%s"' % request.body
    #     return HttpResponse("OK")


    # def api(self, request):
        # ''' Returns 0 for GET, receives and displays emails for POST.'''

        # if request.method == 'GET':
        # return JsonResponse([0, ])

        # # Достаём темы и сложения, чтобы продемонстрировать рпишедший json.
        # new_emails = request.get_json(force=True)
        # for new_email in new_emails:
        #     print("\n\tI've got the email with the following subject:\n\n\t\t{}\n"
        #           .format(new_email['metadata']["Subject"].upper()))
        #     if new_email['attachments']:
        #         print('\t\tAttachments:\n')
        #         for attachment in new_email['attachments']:
        #             print('\t\t\t[Filename]: {:<30} [Size]: {:<10} [MIME]: {:<8}\n'
        #                   .format(attachment['filename'],
        #                           len(attachment['body']),
        #                           attachment['MIME']))

        # # Flask требует возвращать response на POST в правильном формате.
        # resp = make_response('preved', 200)
        # resp.headers['X-Something'] = 'A value'
        # return resp


    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('Hello, World!')