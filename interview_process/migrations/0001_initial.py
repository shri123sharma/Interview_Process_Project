# Generated by Django 4.0.5 on 2023-05-09 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('candidate_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('college', models.CharField(help_text='Enter A College Name', max_length=255)),
                ('college_percent', models.IntegerField()),
                ('branch', models.CharField(max_length=255)),
                ('pass_out_year', models.CharField(blank=True, max_length=100, null=True)),
                ('technology', models.CharField(choices=[('python', 'PYTHON'), ('sql', 'SQL'), ('react', 'REACT')], default='python', max_length=100)),
                ('interview_time', models.DurationField(blank=True, null=True)),
                ('written_test_mark', models.FloatField(blank=True, null=True)),
                ('interview_percentage', models.FloatField(blank=True, null=True)),
                ('pass_or_fail', models.CharField(blank=True, choices=[('no_result', 'NO RESULT'), ('pass', 'PASS'), ('fail', 'FAIL')], default='no_result', max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InteviewQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('python', 'PYTHON'), ('django', 'DJANGO'), ('react', 'REACT'), ('sql', 'SQL'), ('html', 'HTML'), ('css', 'CSS')], default='python', max_length=100)),
                ('question_difficulty_level', models.CharField(choices=[('easy', 'EASY'), ('medium', 'MEDIUM'), ('hard', 'HARD')], default='easy', max_length=50)),
                ('question_answer', models.TextField(blank=True, null=True)),
                ('question_time', models.DurationField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('question_type', models.CharField(choices=[('python', 'PYTHON'), ('react', 'REACT'), ('sql', 'SQL')], default='python', max_length=20)),
                ('question_text', models.TextField(help_text='Please Enter A Question Type')),
                ('question_description', models.TextField(blank=True, help_text='Please Enter A Question Descriptin', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterViewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('questions_result', models.JSONField()),
                ('final_score', models.FloatField(blank=True, null=True)),
                ('candidate_interview', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interview_candidate', to='interview_process.candidate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='interview_process.question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
