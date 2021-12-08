"""
Problem may occur just because of serializer name
it may conflict
"""
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from . import serializer
from .permissions import EditPermission, IsAuthor, IsCandidateUser
from .utils import Util


# Custom JWT Authentication view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


# JWT logout
# class LogoutView(generics.DestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     print('upper')
#     def post(self, request):
#         print('called')
#         try:
#             refresh_token = request.data["refresh_token"]
#             print(refresh_token)
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return response.Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return response.Response(status=status.HTTP_400_BAD_REQUEST)


# User Registration view inheriting APIView class
# class RegisterView(generics.CreateAPIView):
#     serializer_class = serializer.RegisterSerializer
#     queryset = models.User.objects.all()
# permission_classes = [permission.IsAuthenticated]

# def post(self, request):
#     serializers = serializer.UserInfoSerializer(data=request.data)
#     serializers.is_valid(raise_exception=True)
#     serializers.save()
#     return response.Response(serializers.data)

class RegisterView(generics.GenericAPIView):
    serializer_class = serializer.RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = models.User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('tfhrm_api:email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.full_name + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    serializer_class = serializer.EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        # print(token)
        try:
            # print('token1')
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            # print('token2')
            user = models.User.objects.get(id=payload['user_id'])
            # print(email=payload['email'])
            redirect_url = 'https://tf-recruitment.vercel.app/login'
            if user.is_active:
                if not user.email_validated:
                    user.email_validated = True
                    user.save()
                    # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
                    return HttpResponseRedirect(redirect_to=redirect_url)
                else:
                    return HttpResponseRedirect(redirect_to=redirect_url)

            else:
                return Response({'email': 'Activation failed'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserInfoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ProfileUpdateSerializer
    queryset = models.User.objects.all()


# User info View
# Retrieving data from User model data
class UserInfoListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserSerializer

    def get_queryset(self):
        return models.UserInfoModel.objects.all()


# User academic information View
# if user is authenticate user can Retrieve data
# not needed
class UserAcademicInfoListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserAcademicSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        u_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id)


class UserAcademicInfoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        u_id = self.kwargs['uid']
        a_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id, id=a_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# specific User information retrieve
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserDetailsSerializer
    queryset = models.User.objects.all()
    lookup_field = 'id'


# Updating Academic information
# academicInformation update view
class AddAcademicInfoView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    queryset = models.UserAcademicInfoModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Academic Information Update Retrieve & Update View
class AcademicInfoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    queryset = models.UserAcademicInfoModel.objects.all()

    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user__id=id)


class UpdateAcademicInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, EditPermission, IsAuthor]
    serializer_class = serializer.UpdateAcademicInformationSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        u_id = self.kwargs['user__id']

        return models.UserAcademicInfoModel.objects.filter(user__id=u_id, id=id)


# Work Experience CRUD Operations
class AddWorkExperienceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    queryset = models.UserWorkingExperienceModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkInfoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user__id=id)


class UpdateWorkExpInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        w_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserWorkingExperienceModel.objects.filter(user__id=u_id, id=w_id)


# Certification CRUD operations

class AddCertificationsView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserCertificationsSerializer
    queryset = models.UserCertificationsModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CertificationInfoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserCertificationsSerializer

    # queryset = models.UserCertificationsModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserCertificationsModel.objects.filter(user__id=id)


class UpdateCertificationsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserCertificationsSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserCertificationsModel.objects.filter(user__id=u_id, id=c_id)


# Training CRUD operations

class AddTrainingExperienceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    queryset = models.UserTrainingExperienceModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrainingInfoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
    serializer_class = serializer.UserTrainingExperienceSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserTrainingExperienceModel.objects.filter(user__id=id)


class UpdateTrainingExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserTrainingExperienceModel.objects.filter(user__id=u_id, id=c_id)


class SkillsView(generics.CreateAPIView):
    serializer_class = serializer.SkillsSerializer
    queryset = models.SkillsModel.objects.all()
