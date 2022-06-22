from urllib import request

import plivo
from AdminOperationApp.utils import Util
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from UserApp.models import User
from UserApp.permissions import (Authenticated, IsAuthor, IsCandidateUser,
                                 IsEmployee)

from SupportApp import models, serializer


# Create your views here.
class TicketReasonView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.TicketReasonSerializer
    queryset = models.TicketReasonModel.objects.all()


class SupportTicketView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.SupportTicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_employee:
            queryset = models.TicketingForSupportModel.objects.all()
        else:
            queryset = models.TicketingForSupportModel.objects.filter(user=self.request.user)

        return queryset.order_by('-updateTime')
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #get ticketreason from serializer
        ticket_reason=request.data.get('ticketReason')
        ticket_quary=request.data.get('query')
        try:
            email_subject=f'New Support Ticket from {request.user}'
            email_body = render_to_string('emailTemplate/support/support_request_open.html', {
                'applicantName': request.user,
                'ticketReason': ticket_reason,
                'ticketQuery': ticket_quary,
            })
            
            data = {'email_body': email_body, 'to_email': 'mofajjal.techforing@gmail.com',
                    'email_subject': email_subject}
            Util.send_email_body(data)
            return Response({'detail': 'Email Sent.'})
        except:
            return Response({'detail': 'Email Sending failed.'})


class SupportMessageView(generics.ListCreateAPIView):
    permission_classes = [Authenticated, (IsAuthor or IsEmployee)]
    serializer_class = serializer.SupportMessageSerializer

    def get_queryset(self):
        ticketId = self.kwargs['ticketId']
        queryset = models.SupportMessageModel.objects.filter(ticket_id=ticketId)
        return queryset

    def perform_create(self, serializer):
        try:
            image = self.request.user.profile_pic.url
        except:
            image = 'https://careeradmin.techforing.com/media/users/default.jpg'
        serializer.save(ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId']),
                        user=self.request.user, userImage=image, userName=self.request.user)

    def create(self, request, *args, **kwargs):
        ticket = models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId'])

        if (self.request.user == ticket.user) or self.request.user.is_employee:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            if self.request.user==ticket.user:
                to_email='mofajjal.techforing@gmail.com'
                email_subject=f'New Support Message from {ticket.user.full_name}'
                email_body = render_to_string('emailTemplate/support_request.html',{
                    'name': self.request.user.full_name,
                    'message': request.data.get('message'),
                    'email': self.request.user.email,
                    'portalLink': f'https://hrms.techforing.com/recruitment/support',
                    })
            else:
                to_email= ticket.user.email
                email_subject=f'New Support Message from HR'
                email_body = render_to_string('emailTemplate/support/support_request.html',{
                    'name': self.request.user.full_name,
                    'message': request.data.get('message'),
                    'email': 'career@techforing.com',
                    'portalLink': f'https://career.techforing.com/support',
                    })
            try:
                data = {'email_body': email_body, 'to_email': to_email,
                        'email_subject': email_subject}
                Util.send_email_body(data)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'You are not employee or author'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        ticket = models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId'])

        if self.request.user.is_employee or (self.request.user == ticket.user):
            serializer = self.get_serializer(self.get_queryset(), many=True)
            response = serializer.data
            message = models.SupportMessageModel.objects.filter(ticket_id=self.kwargs['ticketId'])
            for msg in message:
                if msg.user != self.request.user:
                    msg.is_read = True
                    msg.save()
            # userName = self.request.user.full_name
            # response.append({'userName':userName})
            return Response(response)
        return Response({'detail': 'You are not employee or author'}, status=status.HTTP_400_BAD_REQUEST)


class CloseTicketView(generics.RetrieveUpdateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.SupportTicketCloseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return models.TicketingForSupportModel.objects.filter(id=self.kwargs['id'])
    
    def perform_update(self, serializer):
        ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['id'])
        ticket_condition=ticket.is_active
        serializer.save()
        try:
            if self.request.user.is_employee:
                portal_link = f'https://career.techforing.com/support'
                to_email=ticket.user.email
                action_by = self.request.user.full_name

            else:
                if self.request.user == ticket.user:
                    portal_link = f'https://hrms.techforing.com/recruitment/support'
                    to_email='mofajjal.techforing@gmail.com'
                    action_by = ticket.user.full_name

            if ticket_condition==True:
                ticket_status = 'Closed'
            else:
                ticket_status = 'Reopened'

            email_subject = f'Support Ticket {ticket_status} by {action_by}'
            email_body = render_to_string('emailTemplate/support/support_request_close_reopen.html', {
                'name': action_by,
                'ticketStatus': ticket_status,
                'portalLink': portal_link,  
            })

            data = {'email_body': email_body, 'to_email': to_email,
                    'email_subject': email_subject}
            Util.send_email_body(data)
            return Response({'detail': 'Email Sent.'})
        except:
            return Response({'detail': 'Email Sending failed.'})
