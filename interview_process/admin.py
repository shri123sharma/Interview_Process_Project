from django.contrib import admin
from interview_process.models import *
# Register your models here.    
admin.site.register(Question)
admin.site.register(Candidate)
admin.site.register(InterviewQuestion)
admin.site.register(Interview)
