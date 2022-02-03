import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from UserApp.models import User
from .pdf_helper import save_pdf
from RecruitmentManagementApp.models import UserJobAppliedModel, OfficialDocumentsModel
from pdfGenerator import serializer
from django.http import HttpResponse


# Create your views here.


class GeneratePDF(APIView):
    def get(self, request, applicationId):
        # print(applicationId)
        checkRedundant = OfficialDocumentsModel.objects.filter(applicationId=applicationId)
        # print(checkRedundant)
        if len(checkRedundant) > 0:
            # data = checkRedundant.get()
            return Response({'detail': 'Already created'})

        else:
            userInfo = UserJobAppliedModel.objects.get(id=applicationId)
            prams = {
                'today': datetime.date.today(),
                'user_info': userInfo,

            }
            file_name, status = save_pdf(prams)

            if not status:
                return Response({'detail': 'pdf generate failed'})
            else:
                OfficialDocumentsModel.objects.create(applicationId=userInfo,
                                                      appointmentLetter=f'/OfficialDocuments/{file_name}.pdf')
                return Response({
                    'status': 200,
                    'path': f'/media/OfficialDocuments/{file_name}.pdf'
                })

    # def get(self, request, applicationId, *args, **kwargs):
    #     # getting the template
    #     pdf = html_to_pdf('pdfGenerator/appointment.html')
    #
    #     # rendering the template
    #     return HttpResponse(pdf, content_type='application/pdf')


class ViewAppointMentLetterView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ViewAppointMentLetterSerializer
    lookup_field = 'applicationId'

    def get_queryset(self):
        queryset = OfficialDocumentsModel.objects.filter(applicationId=self.kwargs['applicationId'])
        return queryset
