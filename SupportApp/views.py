from rest_framework import generics, status, permissions
from SupportApp import serializer, models
from rest_framework.response import Response
from UserApp.permissions import IsAdminUser, IsEmployee, IsCandidateUser, IsAuthor
from UserApp.models import User
from django.conf import settings


# Create your views here.
class SupportTicketView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.SupportTicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_employee:
            queryset = models.TicketingForSupportModel.objects.all().order_by('-updateTime')
        else:
            queryset = models.TicketingForSupportModel.objects.filter(user=self.request.user)

        return queryset


class SupportMessageView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, (IsAuthor or IsEmployee)]
    serializer_class = serializer.SupportMessageSerializer

    def get_queryset(self):
        ticketId = self.kwargs['ticketId']
        queryset = models.SupportMessageModel.objects.filter(ticket_id=ticketId)
        return queryset

    def perform_create(self, serializer):
        image = self.request.user.profile_pic.url
        serializer.save(ticket=models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId']),
                        user=self.request.user, userImage=image, userName=self.request.user)

    def create(self, request, *args, **kwargs):
        ticket = models.TicketingForSupportModel.objects.get(id=self.kwargs['ticketId'])

        if (self.request.user == ticket.user) or self.request.user.is_employee:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
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


class CloseTicketView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
    serializer_class = serializer.SupportTicketCloseSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return models.TicketingForSupportModel.objects.filter(id=self.kwargs['id'])

    # def perform_update(self, serializer):
    #     data = models.TicketingForSupportModel.objects.get(id=self.kwargs['id'])
    #     if data.is_active:
    #         data.is_active = False
    #     else:
    #         data.is_active = True
    #     serializer.save()
