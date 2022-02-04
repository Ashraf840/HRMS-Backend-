from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import plivo


@csrf_exempt
def sendsms_response(smsData):
    client = plivo.RestClient(settings.PLIVO_ID, settings.AUTH_TOKEN)

    # print(smsData['dest_num'])
    client.messages.create(
        src=settings.SENDER_ID,
        dst=smsData['dest_num'],
        text=smsData['msg'])
    return Response({'detail': 'Message Sent.'})
