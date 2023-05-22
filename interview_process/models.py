from django.db import models
# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    class Meta:
        abstract = True
        
class Question(BaseModel):
    Language_Type=[
        ('python','PYTHON'),
        ('react','REACT'),
        ('sql','SQL'),
    ]
    question_type=models.CharField(choices=Language_Type,max_length=20,default='python',)
    question_text=models.TextField(help_text='Please Enter A Question Type',unique=True)
    question_description=models.TextField(help_text='Please Enter A Question Descriptin',null=True,blank=True)

    def __str__(self):
        return self.question_text+self.question_description

    
technology_choices=[
    ("python","PYTHON"),
    ("django","DJANGO"),
    ("sql","SQL"),
    ("react","REACT"),
    ("javascript","JAVASCRIPT"),
]
pass_result=[
    ("no_result","NO RESULT"),
    ("pass","PASS"),
    ("fail","FAIL"),
]
class Candidate(BaseModel):
    candidate_name=models.CharField(max_length=255,)
    email=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    college=models.CharField(max_length=255,help_text='Enter A College Name')
    college_percent=models.FloatField()
    branch=models.CharField(max_length=255)
    pass_out_year=models.CharField(max_length=100, null = True, blank= True)
    technology=models.CharField(max_length=100,choices=technology_choices,default='python')
    interview_time = models.DurationField(null=True,blank=True)
    written_test_mark = models.FloatField(null=True,blank=True)
    interview_percentage = models.FloatField(null=True,blank=True)
    pass_or_fail=models.CharField(max_length=20,choices=pass_result,default='no_result',null=True,blank=True)

    def __str__(self):
        return self.candidate_name
    
question_type=[
    ('python','PYTHON'),
    ('django','DJANGO'),
    ('react','REACT'),
    ('sql','SQL'),
    ('html','HTML'),
    ('css','CSS'),
]
dificulty_level=[
    ('easy','EASY'),
    ('medium','MEDIUM'),
    ('hard','HARD'),
]

class InterviewQuestion(BaseModel):
    question_type=models.CharField(max_length=100,choices=question_type,default='python')
    question_difficulty_level=models.CharField(max_length=50,choices=dificulty_level,default='easy')
    question_text=models.TextField(unique=True)
    question_description=models.TextField(null=True,blank=True,) 
    question_answer=models.TextField(null=True,blank=True)
    question_time =models.DurationField(null=True)
    pointer = models.PositiveIntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.question_text+"/n"+self.question_type
    
class Interview(BaseModel):
    candidate_interview=models.ForeignKey(Candidate,null=True,blank=True,related_name='interview_candidate',on_delete=models.CASCADE)
    questions_result=models.JSONField()
    final_score = models.FloatField(null=True, blank=True,default=0)

    def __str__(self):
        return str(self.final_score)
    
class QuestionType(BaseModel):
    question=models.CharField(max_length=200,null=True,blank=True)
    question_type=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.question_type