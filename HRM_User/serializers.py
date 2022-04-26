from asyncore import read
from multiprocessing import managers
from rest_framework import serializers
from HRM_User import models as hrm_user_model
from UserApp import permissions as custom_permission
from serializer_permissions import serializers as permission_ser
from HRM_Admin import serializer as hrm_admin_ser


class EmployeeTrainingResponseResultSerializer(serializers.ModelSerializer):
    """
    Employee training information response will be serialized here
    """

    class Meta:
        model = hrm_user_model.EmployeeTrainingResponseResultModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }


#  ================= Employee Leave Section =================
class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):
    status = permission_ser.CharField(permission_classes=(custom_permission.IsHrOrReadOnly,), hide=True)

    class Meta:
        model = hrm_user_model.LeaveRequestModel
        fields = '__all__'
        extra_kwargs = {
            'no_of_days': {'read_only': True},
            # 'status': {'read_only': True},
            'approved_by': {'read_only': True},
            'employee': {'read_only': True},
        }

#  ================= Employee Resignation Section =================

#exit interview section
class ExitInterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_user_model.ExitInterviewQuestionModel
        fields = '__all__'
        
class ExitInterviewAnswerSerializer(serializers.ModelSerializer):
    # resignation=EmployeeResignationRequestSerializer(source='exit_interview_answer_employee')
    # question=ExitInterviewQuestionSerializer(read_only=True,source='question.question')
    # employee=hrm_admin_ser.EmployeeInformationListSerializer(read_only=True)
    class Meta:
        model = hrm_user_model.ExitInterviewAnswerModel
        fields = '__all__'
        extra_fields = ('question',)
        
class EmployeeResignationRequestSerializer(serializers.ModelSerializer):
    answers=ExitInterviewAnswerSerializer(source='answer_employee',many=True)
    class Meta:
        model = hrm_user_model.ResignationModel
        fields = ['employee','reason','noticeDate','resignationDate','resignatioAcceptDate','answers']
        extra_kwargs = {
            'employee': {'read_only': True},
            'resignationstaus': {'read_only': True},
            'resignatioAcceptDate': {'read_only': True},
        }
    def create(self, validated_data):
        answers_data=validated_data.pop('answer_employee')
        employee_resignation_request=hrm_user_model.ResignationModel.objects.create(**validated_data)
        resignation_data=hrm_user_model.ResignationModel.objects.filter().first()
        check=set()
        #get the lentgh of the exitquestion data record
        total_len=hrm_user_model.ExitInterviewQuestionModel.objects.all().count()
        counter=0
        for answer_data in answers_data:
            if answer_data['question'] not in check:
                check.add(answer_data['question'])
                counter+=1
                hrm_user_model.ExitInterviewAnswerModel.objects.create(resignation=resignation_data,**answer_data)
            # hrm_user_model.ExitInterviewAnswerModel.objects.create(resignation=employee_resignation_request.employee,**answer_data)
        if counter!=total_len:
            hrm_user_model.ResignationModel.objects.filter(id=resignation_data.id).delete()
            serializers.ValidationError("All the questions are not answered")
        return employee_resignation_request
    # def get_answers(self, obj):
    #         print(obj)
    #         answer_employee= hrm_user_model.ExitInterviewAnswerModel.objects.filter(employee=obj.employee)
    #         serializer = ExitInterviewAnswerSerializer(answer_employee, many=True)
    #         return serializer.data