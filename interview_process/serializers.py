from rest_framework import serializers
from interview_process.models import *

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['id','question_type','question_text','question_description']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Candidate
        fields=['id','candidate_name','email','phone_number','college','college_percent','branch','pass_out_year','technology','interview_time','written_test_mark','interview_percentage','pass_or_fail']

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=InterviewQuestion
        fields=['id','question_text','question_type','question_difficulty_level','question_answer','question_description','question_time','created_date','updated_date']

class InterviewSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Interview
        fields=['candidate_interview_id','questions_result','final_score','created_date','updated_date',]

class InterviewScoreSerilaizer(serializers.ModelSerializer):

    class Meta:
        model=Interview
        fields=['candidate_interview_id','final_score','created_date']



    
