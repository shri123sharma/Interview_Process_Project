from random import sample
import random
from rest_framework.views import APIView
from interview_process.models import *
from interview_process.serializers import *
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse

# Create your views here.
class QuestionView(APIView):
    def get(self,request,*args,**kwargs): 
        dict_response={}
        question_type = self.request.query_params.get('question_type')
        if question_type:
            data_str_fixed = question_type.replace("'", '"')
            my_dict = json.loads(data_str_fixed)
            for question_type,question_number in my_dict.items():
              if question_type==question_type:
                  question_pks = Question.objects.filter(question_type=question_type).values_list('id', flat=True)
                  question_pks_length=len(question_pks)
                  if question_number>question_pks_length:
                    return HttpResponse(f"{question_type} length in more then database record")
                  random_id = random.sample(list(question_pks),question_number)
                  random_questions = Question.objects.filter(pk__in=random_id)
                  serializer = QuestionSerializer(random_questions,many=True)
                  dict_response[f"{question_type} Question"] = serializer.data
            return Response(dict_response,status=status.HTTP_200_OK)
        return Response("Query parameter not provided")
    
    def post(self, request):
      request_data=request.data
      if not request_data:
        return  Response({'message':'request data is missing'},status=status.HTTP_400_BAD_REQUEST)
      
      if 'question_type' not in list(request_data.keys()) or 'question_text' not in list(request_data.keys()): 
          return Response({'messgae':'question_type and question_text both are required'},status=status.HTTP_400_BAD_REQUEST)
      
      if 'question_type' in list(request_data.keys()) or 'question_text' in list(request_data.keys()):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                       
                  
    def put(self,request,question_id):
      try:
        question=Question.objects.get(id=question_id)
        question_serializer=QuestionSerializer(question,data=request.data)
        if question_serializer.is_valid():
          question_serializer.save()
          return Response(question_serializer.data,status=status.HTTP_200_OK)
      except Question.DoesNotExist:
          return Response({"error": "Object Does Not Exists."}, status=status.HTTP_404_NOT_FOUND)
      
    def delete(self, request, question_id,):
        try:
          interview_question=Question.objects.get(id=question_id)
          interview_question.delete()  
        except Question.DoesNotExist:
           return Response("Object Does Not Exist",status=status.HTTP_404_NOT_FOUND)
        return Response("Questions Is Deletd",status=status.HTTP_204_NO_CONTENT)
      
class  CandidateRegister(APIView):  
    def get(self,request):
      candidate=Candidate.objects.all()
      candidate_seralizer=CandidateSerializer(candidate,many=True)
      return Response(candidate_seralizer.data,status=status.HTTP_200_OK)
   
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class InterviewQuestionView(APIView): 
    def get(self,request):
      question_type = self.request.query_params.get('question_type')
      question_difficulty_level=self.request.query_params.get('question_difficulty_level')
      if question_type:
        queryset=InterviewQuestion.objects.filter(question_type=question_type)
        if question_difficulty_level=='easy':
          queryset=queryset.filter(question_difficulty_level=question_difficulty_level)
          question_serilaizer=InterviewQuestionSerializer(queryset,many=True)
        elif question_difficulty_level=='medium':
          queryset=queryset.filter(question_difficulty_level=question_difficulty_level)
          question_serilaizer=InterviewQuestionSerializer(queryset,many=True)
        elif question_difficulty_level=='hard':
          queryset=queryset.filter(question_difficulty_level=question_difficulty_level)
          question_serilaizer=InterviewQuestionSerializer(queryset,many=True)
        question_serilaizer=InterviewQuestionSerializer(queryset,many=True)
        return Response(question_serilaizer.data,status=status.HTTP_200_OK)
      return Response('Query Parameter Is Not Provided')
    
    def post(self,request,*args,**kwargs):
      request_data=request.data
      if not request_data:
        return  Response({'message':'request data is missing'},status=status.HTTP_400_BAD_REQUEST)
      
      if 'question_type' not in list(request_data.keys()) or 'question_text' not in list(request_data.keys()) or 'question_difficulty_level' not in list(request_data.keys()): 
        return Response({'messgae':'question_type and question_text and question_diificulty are required'},status=status.HTTP_400_BAD_REQUEST)
      
      interview_question=InterviewQuestionSerializer(data=request.data)
      if interview_question.is_valid():
          interview_question.save()
          return Response(interview_question.data, status=status.HTTP_201_CREATED)
      return Response(interview_question.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,question_id):
      try:
        interview_question=InterviewQuestion.objects.get(id=question_id)
        question_serilaizer=InterviewQuestionSerializer(interview_question,data=request.data)
        if question_serilaizer.is_valid():
          question_serilaizer.save()
          return Response(question_serilaizer.data,status=status.HTTP_200_OK)
      except InterviewQuestion.DoesNotExist:
          return Response({"error": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
      
    def delete(self, request, question_id,):
        try:
          interview_question= InterviewQuestion.objects.get(id=question_id)
          interview_question.delete()  
        except InterviewQuestion.DoesNotExist:
           return Response("Object Does Not Exist",status=status.HTTP_404_NOT_FOUND)
        return Response("Interview Questions Deletd",status=status.HTTP_204_NO_CONTENT)
    
class MyModelPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 100

class InterviewView(APIView):
    def get(self,request):
      date_wise = self.request.query_params.get('created_date')
      if date_wise is None:
        queryset=Interview.objects.all()
        paginator = MyModelPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        interview_score=InterviewScoreSerilaizer(paginated_queryset,many=True)
      if date_wise:
         queryset=Interview.objects.filter(created_date__date=date_wise)
         paginator = MyModelPagination()
         paginated_queryset = paginator.paginate_queryset(queryset, request)
         interview_score=InterviewScoreSerilaizer(queryset,many=True)
      return paginator.get_paginated_response(interview_score.data)

      
    def post(self, request):
        request_data = request.data
        if not request_data:
          return  Response({'message':'request data is missing'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'candidate_interview_id' not in list(request_data.keys()) or 'questions_result' not in list(request_data.keys()):
          return Response({'messgae':'candidate and question_result both are required'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'candidate_interview_id' in list(request_data.keys()) or 'questions_result' in list(request_data.keys()):
          candidate_id = int(request_data.get('candidate_interview_id'))
          question_data = request_data.get('questions_result') 
          question_data =json.loads(question_data)
          interview = Interview.objects.create(
              candidate_interview_id=candidate_id,
              questions_result=question_data
          ) 
          total_score = 0
          for data in question_data:
              question_id = data.get('question_id')
              pointer = data.get('pointer')
              InterviewQuestion.objects.filter(id=question_id,pointer=pointer)
              total_score += pointer
          interview.final_score = total_score
          interview.save()
          interview_serializer = InterviewSerilaizer(instance=interview,data=request_data)
          if interview_serializer.is_valid():
            interview_serializer.save()
            return Response(interview_serializer.data, status=status.HTTP_201_CREATED)  
          
