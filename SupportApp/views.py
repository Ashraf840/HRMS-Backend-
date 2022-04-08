from rest_framework import generics, status, permissions
from SupportApp import serializer, models
from rest_framework.response import Response
from UserApp.permissions import IsEmployee, IsCandidateUser, IsAuthor, Authenticated
from UserApp.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import plivo
from AdminOperationApp.utils import Util

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
            email_body = f'{request.user} has opend a new ticket\n' \
                         f'TicketReason is: {ticket_reason}\n' \
                         f'TicketQuary is: {ticket_quary}'\
                         

            data = {'email_body': email_body, 'to_email': 'faruk.techforing@gmail.com',
                    'email_subject': 'New ticket.'}
            Util.send_email(data)
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
                to_email='faruk.techforing@gmail.com'
            else:
                to_email= ticket.user.email
            email_body=request.data.get('message')
            try:
                # email_body = f'Your ticket has been closed'
                data = {'email_body': email_body, 'to_email': to_email,
                        'email_subject': 'New message.'}
                Util.send_email(data)
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
        serializer.save()
        ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['id'])
        user_email=ticket.user.email
        try:
            email_body = f'Your ticket has been closed'
            data = {'email_body': email_body, 'to_email': user_email,
                    'email_subject': 'Ticket Closed.'}
            Util.send_email(data)
            return Response({'detail': 'Email Sent.'})
        except:
            return Response({'detail': 'Email Sending failed.'})