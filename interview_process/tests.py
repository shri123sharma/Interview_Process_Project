from django.test import TestCase, Client
import json
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from interview_process.models import *
from rest_framework.serializers import *
from interview_process.serializers import *
from datetime import date

# .........................................................Question_get_api_test_cases.............................
class QuestionGetTestCase(APITestCase):
    def setUp(self):
      self.client = APIClient()
      self.url = reverse('question')
      Question.objects.create(question_type='python', question_text='What is python',question_description="")   
      Question.objects.create(question_type='sql', question_text='sql first question',question_description='')
      Question.objects.create(question_type='react',question_text='react first question',question_description="")
      
    def test_filter_by_question_type_all_object(self):
        question_type = {"python": 1,"sql":1,"react":1}
        url = reverse('question') + f'?question_type={question_type}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_my_view_without_param(self):
        url = reverse('question')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Query parameter not provided')

    def test_question_length(self):
        question_type = {'python': 10,'sql':10,'react':10}
        url = reverse('question')+f'?question_type={question_type}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'length in more then database record')

# ...........................................................question_post_api_test_case...........................
class QuestionPostTestCase(APITestCase):
    def setUp(self):  
        self.client = APIClient()
        self.url = reverse('question')

    def test_post_request_with_missing_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_create_question(self):
        data = {
            'question_type':'python',
            'question_text':'python_firstcdcdcccdccc',
            'question_description':'question_description',
            
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_some_data_missing(self):
        data={
            'question_type':'python',
            'question_description':'',
        }
        response=self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_unique_question_text(self):
        Question.objects.create(
            question_type='python',
            question_text='python_first',
            question_description='question_description',   
        )
        data = {
            'question_type':'python',
            'question_text':'python_first',
            'question_description':'question_description',
           
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('question_text' in response.data)
        self.assertEqual(response.data['question_text'][0], "question with this question text already exists.")

# .......................................................Question_put_api_test_case..........................
class QuestionPutAPiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.obj = Question.objects.create(
            question_type='python',
            question_text='this is django framework',
            question_description='',

        )
        self.url = reverse('question',args=[self.obj.pk])
        self.data = {
            'question_type':'python',
            'question_text':'django_first',
            'question_description':'django_description_question',
        }
    def test_interview_question_update(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ................................................question_put_api_404>......................................
class QuestionPutAPi404TestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('question',args=[999])
        self.data = {
            'question_type':'python',
            'question_text':'django_first',
            'question_description':'django_description_question',
           
        }
    def test_update_exist_object(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ................................................question_delete_api_test_case..............................
class QuestionDeleteApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('question')

    def test_question_delete_api_test_case(self):
        question_obj = Question.objects.create(
            question_type='python',
            question_text='this is django framework',
            question_description='',     
        )
        self.urls = reverse('question',args=[question_obj.id])
        response=self.client.delete(self.urls)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class QuestionDeleteApi404TestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('question')

    def test_delete_nonexistent_object(self):
        self.urls = reverse('question',args=[999])
        response=self.client.delete(self.urls)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client = APIClient()
        self.url = reverse('question')

    def test_delete_nonexistent_object(self):
        self.urls = reverse('question',args=[999])
        response=self.client.delete(self.urls)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

       
#.................................................interview_question_get_api_test_cases......................................
class InterviewQuestionGetApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interview_question')
        InterviewQuestion.objects.create(question_text='python_first',question_type='python', question_difficulty_level='easy',pointer=5)
        InterviewQuestion.objects.create(question_text='python_second',question_type='python', question_difficulty_level='medium',pointer=5)
        InterviewQuestion.objects.create(question_text='python_third',question_type='python', question_difficulty_level='hard',pointer=5)
        InterviewQuestion.objects.create(question_text='sql_first',question_type='sql', question_difficulty_level='easy',pointer=5)
        InterviewQuestion.objects.create(question_text='sql_second',question_type='sql', question_difficulty_level='medium',pointer=5)
        InterviewQuestion.objects.create(question_text='sql_third',question_type='sql', question_difficulty_level='hard',pointer=5)
        InterviewQuestion.objects.create(question_text='react_first',question_type='react', question_difficulty_level='easy',pointer=5)
        InterviewQuestion.objects.create(question_text='react_second',question_type='react', question_difficulty_level='medium',pointer=5)
        InterviewQuestion.objects.create(question_text='react_third',question_type='react', question_difficulty_level='hard',pointer=5)

    def test_my_view_without_param(self):
        url = reverse('interview_question')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Query Parameter Is Not Provided')

    def test_filter_question_python_difficulty_easy(self):
        question_type='python'
        question_difficulty_level='easy'
        url=reverse('interview_question')+f'?question_type={question_type}&question_difficulty_level={question_difficulty_level}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_question_python_difficulty_medium(self): 
        question_type='python'
        question_difficulty_level='medium'
        url=reverse('interview_question')+f'?question_type={question_type}&question_difficulty_level={question_difficulty_level}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_question_python_difficulty_hard(self):
        question_type='python'
        question_difficulty_level='hard'
        url=reverse('interview_question')+f'?question_type={question_type}&question_difficulty_level={question_difficulty_level}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
# .............................................interview_question_post_api_test_case............................
class InterviewQuestionPostApiTestCase(APITestCase):
    def setUp(self):
      self.client = APIClient()
      self.url = reverse('interview_question')

    def test_post_request_with_missing_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_with_some_data_missing(self):
        data={
            'question_type':'python',
            'question_description':'',
        }
        response=self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,400)

    def test_create_interview_question(self):
        data = {
            'question_type':'python',
            'question_difficulty_level':'easy',
            'question_text':'python_first',
            'question_description':'question_description',
            'question_answer':"python is interpeter language",
            'question_time':30,
            'pointer':5
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InterviewQuestion.objects.get().question_text, 'python_first')

    def test_unique_question_text(self):
        InterviewQuestion.objects.create(
            question_type='python',
            question_difficulty_level='easy',
            question_text='python_first',
            question_description='question_description',
            question_answer='python is interpeter language',
             
        )
        data = {
            'question_type':'python',
            'question_difficulty_level':'easy',
            'question_text':'python_first',
            'question_description':'question_description',
            'question_answer':"python is interpeter language",
            'question_time':30,
            'pointer':5
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('question_text' in response.data)
        self.assertEqual(response.data['question_text'][0], "interview question with this question text already exists.")

# .......................................Interview_question_put_api..........................................
class InterviewQuestionPutApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.obj = InterviewQuestion.objects.create(
            question_type='python',
            question_difficulty_level='easy',
            question_text='this is django framework',
            question_description='',
            question_answer='djnago',

        )
        self.url = reverse('interview_question',args=[self.obj.pk])
        self.data = {
            'question_type':'django',
            'question_difficulty_level':'medium',
            'question_text':'django_first',
            'question_description':'django_description_question',
            'question_answer':"django is a framework with python",   
        }

    def test_interview_question_update(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

# ................................................interview_question_put_api_404_test_case............................
class InterviewQuestionPutApi404Testcase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interview_question',args=[999])
        self.data = {
            'question_type':'django',
            'question_difficulty_level':'medium',
            'question_text':'django_first',
            'question_description':'django_description_question',
            'question_answer':"django is a framework with python",
           
        }
    def test_update_exist_object(self):
        response = self.client.put(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#.............................................interview_question_delete_api_test_case...........................

class InterviewQuestionDeleteAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interview_question')

    def test_delete_object(self):
        object_to_delete = InterviewQuestion.objects.create(
            question_type='python',
            question_difficulty_level='easy',
            question_text='this is django framework',
            question_description='',
            question_answer='djnago',
            
        )
        self.urls = reverse('interview_question',args=[object_to_delete.id])
        response=self.client.delete(self.urls)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# .....................................interview_question_delete_api_404_test_case............................

class InterviewQuestionDelete404ApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('interview_question')

    def test_delete_nonexistent_object(self):
        self.urls = reverse('interview_question',args=[999])
        response=self.client.delete(self.urls)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

# ......................................candidate_get_api_test_cases........................................................
class CandidateGetAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('candidate_register')
        self.candidate1 = Candidate.objects.create(
            candidate_name='John Doe', 
            email='john.doe@example.com',
            phone_number='12345677890',
            college='sirts',
            college_percent=64.4,
            branch='ME'
            )
    
    def test_get_all_candidates(self):
        response = self.client.get(self.url)
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

# .....................................................candidate_post_api_test_cases.............................

class CandidatesPostApiTestCase(APITestCase):  
    def setUp(self):
      self.client = APIClient()
      self.url = reverse('candidate_register')

    def test_create_candidate_registration(self):
        data = {
            'candidate_name':'user_1',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'college':'sirts',
            'college_percent':64.0,
            'branch':'Me',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.get().email, 'test@example.com')

    def test_unique_email(self):
        Candidate.objects.create(
            email='test@example.com',
            phone_number='1234567890',
            college='sirts',
            college_percent=64.0,
            branch='Me',
        )
        data = {
            'candidate_name':'user_1',
            'email': 'test@example.com',
            'phone_number': '0987654321',
            'college':'sirts',
            'college_percent':64.0,
            'branch':'Me',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('email' in response.data)
        self.assertEqual(response.data['email'][0], 'candidate with this email already exists.')

# ................................................interview_get_api_test_case................................
class InterviewGetAPiTestCase(APITestCase):
    def setup(self):
      self.client = APIClient()
      self.url = reverse('interview')
      Interview.objects.create(candidate_interview='rahul',final_score=18.0,created_date='2023-05-17')

    def test_filter_by_created_date(self):
        created_date='2023-05-17'
        url = reverse('interview') + f'?created_date={created_date}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class InterviewGetApiTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('interview')

    def test_query_parameter_with_none_value(self):
        response = self.client.get(self.url) 
        self.assertEqual(response.status_code, 200) 

    def test_query_parameter_created_date(self):
        created_date='2023-05-17'
        url = reverse('question')+f'?created_date={created_date}'
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200) 

# ..................................................interview_post_api_test_case..............................
class InterviewPostApiTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('interview')
        self.test_candidate = Candidate.objects.create(candidate_name='test_1',
                                                       email='test_1@example.com',
                                                       phone_number='2627666336',
                                                       college='sirts',
                                                       college_percent=60.7,
                                                       branch='me'
                                                       ) 

    def test_post_request_with_missing_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)


    def test_post_request_with_missing_parameter(self):
        request_data = {
            'candidate_interview_id': 1,
        }
        response = self.client.post(self.url, json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print('question_result_candidate_id 400')

    def test_post_request_with_missing_parameter(self):
        test_data = {
            'question_result': '[{"question_id":2,"pointer":3},{"question_id":5,"pointer":2},{"question_id":1,"pointer":1}]'
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 400)
    

    def test_valid_data_post_create(self):
        valid_payload={
            'candidate_interview_id':self.test_candidate.id,
            'questions_result':'[{"question_id":2,"pointer":3},{"question_id":5,"pointer":2},{"question_id":1,"pointer":1}]'
        }
        response = self.client.post(self.url, json.dumps(valid_payload),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

      