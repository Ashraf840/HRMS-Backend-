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
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistedToken
from . import models
from . import serializer
from .permissions import EditPermission, IsAuthor, IsCandidateUser, Authenticated, CandidateAdminAuthenticated
from .utils import Util


# Custom JWT Authentication view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializer.CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class HRMCustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Authentication for Employee
    """
    serializer_class = serializer.HRMCustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


# JWT logout
class BlacklistTokenUpdateView():
    permission_classes = [Authenticated]
    authentication_classes = ()

    def post(self, request):
        print(request)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(views.APIView):
    serializer_class = serializer.LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        #
        # return Response(status=status.HTTP_204_NO_CONTENT)


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

        email_body = f'Hi {user.full_name},\n' \
                     f'Were happy you signed up for Techforing Career. To start exploring the Techforing Career Please confirm your email address. ' \
                     f'Verification link {absurl}'

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verification Email'}

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
            redirect_url = 'https://career.techforing.com/auth'
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


class EmployeeEmailVerifyView(views.APIView):
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
            print(payload)
            user = models.User.objects.get(id=payload['user_id'])
            # print(email=payload['email'])
            redirect_url = 'https://hrms.techforing.com/login'
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


class UserProfileCompletionPercentageView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserProfileCompletionPercentageSerializer

    def get_queryset(self):
        # print(self.request.user.id)
        query = models.User.objects.filter(id=self.request.user.id)
        return query

    def list(self, request, *args, **kwargs):
        response = self.get_serializer(self.get_queryset(), many=True)
        responseData = response.data
        user_id = self.request.user.id
        percentage = 20
        careerObjective = models.CareerObjectiveModel.objects.filter(user_id=user_id).count()
        academicInfo = models.UserAcademicInfoModel.objects.filter(user_id=user_id).count()
        workInfo = models.UserWorkingExperienceModel.objects.filter(user_id=user_id).count()
        trainingInfo = models.UserTrainingExperienceModel.objects.filter(user_id=user_id).count()
        certificateInfo = models.UserCertificationsModel.objects.filter(user_id=user_id).count()
        skillsInfo = models.UserSkillsModel.objects.filter(user_id=user_id).count()
        if academicInfo > 0:
            if academicInfo > 2:
                percentage += 30
            else:
                percentage += academicInfo * 15
        if careerObjective > 0:
            percentage += 10

        if workInfo > 0:
            percentage += 10

        if trainingInfo > 0:
            percentage += 10

        if certificateInfo > 0:
            percentage += 10

        if skillsInfo > 0:
            percentage += 10

        if percentage > 100:
            percentage = 100

        return Response(percentage)


class DesignationView(generics.ListCreateAPIView):
    permission_classes = [CandidateAdminAuthenticated]
    serializer_class = serializer.DesignationSerializer
    queryset = models.UserDesignationModel.objects.all()


class UpdateUserInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.ProfileUpdateSerializer
    queryset = models.User.objects.all()

    # parser_classes = [parsers.MultiPartParser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# User info View
# Retrieving data from User model data
# class UserInfoListView(generics.ListCreateAPIView):
#     permission_classes = [Authenticated]
#     serializer_class = serializer.UserSerializer
#
#     def get_queryset(self):
#         return models.EmployeeInfoModel.objects.all()


# User academic information View
# if user is authenticate user can Retrieve data
# not needed
class DepartmentView(generics.ListCreateAPIView):
    permission_classes = [CandidateAdminAuthenticated]
    serializer_class = serializer.UserDepartmentSerializer
    queryset = models.UserDepartmentModel.objects.all()


class EducationLevelView(generics.ListAPIView):
    permission_classes = [CandidateAdminAuthenticated]
    serializer_class = serializer.EducationLevelSerializer
    queryset = models.EducationLevelModel.objects.all()


class DegreeTitleView(generics.ListAPIView):
    """
    return data using the filter queries based on education level
    """
    permission_classes = [CandidateAdminAuthenticated]
    serializer_class = serializer.DegreeTitleSerializer

    def get_queryset(self):
        educationLevel_id = self.kwargs['educationLevel']
        return models.DegreeTitleModel.objects.filter(educationLevel=educationLevel_id)


class UserAcademicInfoListView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserAcademicSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        u_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id)


class UserAcademicInfoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        u_id = self.kwargs['uid']
        a_id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user_id=u_id, id=a_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CareerObjectiveView(generics.CreateAPIView):
    permission_classes = [Authenticated, EditPermission]
    serializer_class = serializer.CareerObjectiveSerializer

    def get_queryset(self):
        if self.request.user.is_hr or self.request.user.is_superuser:
            queryset = models.CareerObjectiveModel.objects.all()
        else:
            queryset = models.CareerObjectiveModel.objects.filter(user=self.request.user)
        return queryset

    # lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CareerObjectiveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [Authenticated, EditPermission]
    serializer_class = serializer.CareerObjectiveSerializer
    lookup_field = 'user_id'
    queryset = models.CareerObjectiveModel.objects.all()


# specific User information retrieve
class UserLoginDetailView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserLoginDetailsSerializer

    def get_queryset(self):
        queryset = models.User.objects.filter(id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_queryset(), many=True)
        user = ser.data[0]
        return Response(user)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserDetailsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_hr or user.is_superuser or user.is_hr:
            queryset = models.User.objects.all()
        else:
            queryset = models.User.objects.filter(id=self.request.user.id)
        return queryset


# Updating Academic information
# academicInformation update view
class AddAcademicInfoView(generics.CreateAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    queryset = models.UserAcademicInfoModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Academic Information Update Retrieve & Update View
class AcademicInfoListView(generics.ListAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer
    queryset = models.UserAcademicInfoModel.objects.all()

    def get_queryset(self):
        id = self.kwargs['id']
        if self.request.user.id == id:
            return models.UserAcademicInfoModel.objects.filter(user__id=self.request.user.id)
        elif self.request.user.is_hr:
            return models.UserAcademicInfoModel.objects.filter(user__id=id)


class UpdateAcademicInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated, EditPermission, IsAuthor]
    serializer_class = serializer.UpdateAcademicInformationSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        u_id = self.kwargs['user__id']

        return models.UserAcademicInfoModel.objects.filter(user__id=self.request.user.id, id=id)


# Work Experience CRUD Operations
class AddWorkExperienceView(generics.CreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    queryset = models.UserWorkingExperienceModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkInfoListView(generics.ListAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserAcademicSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserAcademicInfoModel.objects.filter(user__id=id)


class UpdateWorkExpInfoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserWorkExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        w_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserWorkingExperienceModel.objects.filter(user__id=self.request.user.id, id=w_id)


# Certification CRUD operations

class AddCertificationsView(generics.CreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserCertificationsSerializer
    queryset = models.UserCertificationsModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CertificationInfoListView(generics.ListAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserCertificationsSerializer

    # queryset = models.UserCertificationsModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserCertificationsModel.objects.filter(user__id=id)


class UpdateCertificationsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserCertificationsSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserCertificationsModel.objects.filter(user__id=self.request.user.id, id=c_id)


# Training CRUD operations

class AddTrainingExperienceView(generics.CreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    queryset = models.UserTrainingExperienceModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TrainingInfoListView(generics.ListAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.UserTrainingExperienceSerializer

    # queryset = models.UserAcademicInfoModel.objects.all()
    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserTrainingExperienceModel.objects.filter(user__id=id)


class UpdateTrainingExperienceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.UserTrainingExperienceSerializer
    # queryset = models.UserAcademicInfoModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        c_id = self.kwargs['id']
        u_id = self.kwargs['user__id']
        return models.UserTrainingExperienceModel.objects.filter(user__id=self.request.user.id, id=c_id)


class AddUserSkillsView(generics.ListCreateAPIView):
    """
    adding user skills if skill is not in the skill table automatically new will add to the database
    """
    permission_classes = [Authenticated]
    serializer_class = serializer.UserSkillsSerializer
    queryset = models.UserSkillsModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        skills = request.data.get('skills', [])
        # print(skills)
        for skill in skills:
            models.SkillsModel.objects.get_or_create(skillName=skill)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


class UpdateUserSkillsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updating user skills if skill is not in the skill table automatically new will add to the database
    """
    permission_classes = [Authenticated]
    serializer_class = serializer.UserSkillsSerializer
    queryset = models.UserSkillsModel.objects.all()
    lookup_field = 'user_id'

    # def perform_update(self, serializer):
    #     serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            skills = request.data.getlist('skills')
        except:
            skills = request.data.get('skills')

        for skill in skills:
            models.SkillsModel.objects.get_or_create(skillName=skill)

        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SkillsView(generics.ListCreateAPIView):
    serializer_class = serializer.SkillsSerializer
    queryset = models.SkillsModel.objects.all()


#
# """
# Document submission section during -> DocumentSubmissionView
# User will upload during recruitment process -> ReferenceInformationView
#
# """
#
#
# class DocumentSubmissionView(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.DocumentationSubmissionSerializer
#     queryset = models.DocumentSubmissionModel.objects.all()
#
#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)
#
#     def create(self, request, *args, **kwargs):
#         job_id = self.kwargs['job_id']
#
#         try:
#             data = UserJobAppliedModel.objects.get(userId=self.request.user, id=job_id)
#             if data.jobProgressStatus.status == 'Document':
#                 checkRedundancy = models.DocumentSubmissionModel.objects.filter(user=self.request.user)
#                 # print(checkRedundancy)
#                 if checkRedundancy.exists():
#                     return Response({'detail': 'Your data has been updated already.'},status=status.HTTP_400_BAD_REQUEST)
#
#                 serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
#                     # print(serializer)
#                 serializer.is_valid(raise_exception=True)
#                 self.perform_create(serializer)
#                 headers = self.get_success_headers(serializer.data)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#             else:
#                 return Response({'detail': 'You are not selected for Document Submission'},status=status.HTTP_403_FORBIDDEN)
#                 # more validation will be a plus.
#
#
#         except:
#             return Response({'detail': 'You are not selected to proceed.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
#         # # print(serializer)
#         # serializer.is_valid(raise_exception=True)
#         # self.perform_create(serializer)
#         # headers = self.get_success_headers(serializer.data)
#
#
# class DocumentDetailsView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.DocumentationSubmissionSerializer
#     def get_queryset(self):
#         applied_job = self.kwargs['applied_job']
#         queryset = models.DocumentSubmissionModel.objects.filter(user=self.request.user,)
#
#
# class DocumentSubmissionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsAuthor]
#     serializer_class = serializer.DocumentationSubmissionSerializer
#     # queryset = models.DocumentSubmissionModel.objects.all()
#     lookup_field = 'id'
#
#     # def perform_create(self, serializer):
#     #     return serializer.save(user=self.request.user)
#
#     def get_queryset(self):
#         id = self.kwargs['id']
#         return models.DocumentSubmissionModel.objects.filter(id=id, user_id=self.request.user.id)
#
#
# class ReferenceInformationView(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.ReferenceInformationSerializer
#     queryset = models.ReferenceInformationModel.objects.all()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def create(self, request, *args, **kwargs):
#         job_id = self.kwargs['job_id']
#         try:
#             data = UserJobAppliedModel.objects.get(userId=self.request.user, id=job_id)
#             if data.jobProgressStatus == 'reference':
#                 serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
#                 # print(serializer)
#                 serializer.is_valid(raise_exception=True)
#                 self.perform_create(serializer)
#                 headers = self.get_success_headers(serializer.data)
#                 data.jobProgressStatus = 'verification'
#                 data.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#             else:
#                 return Response({'detail': 'Not selected for Documentation'},
#                                 status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#         except:
#             return Response({'detail': 'No Data found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#
#
# class ReferenceInformationUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsAuthor]
#     serializer_class = serializer.ReferenceInformationSerializer
#
#     lookup_field = 'id'
#
#     def get_queryset(self):
#         id = self.kwargs['id']
#         return models.ReferenceInformationModel.objects.filter(id=id, user_id=self.request.user.id)


"""
Change and Reset Password section
"""


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializer.ChangePasswordSerializer
    model = models.User
    permission_classes = [Authenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
