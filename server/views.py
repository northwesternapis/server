from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from server.serializers import *
from server.models import *
from django.http import HttpResponse
import datetime

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def get_subjects(request):
    subjects = Subject.objects.order_by('symbol', 'name').distinct('symbol', 'name').values('symbol', 'name')
    serializer = SubjectSerializer(subjects, many=True)
    return JSONResponse(serializer.data)

def get_schools(request):
    schools = School.objects.all()
    serializer = SchoolSerializer(schools, many=True)
    return JSONResponse(serializer.data)

def get_terms(request):
    terms = Term.objects.filter(shopping_cart_date__lt=datetime.date.today())
    serializer = TermSerializer(terms, many=True)
    return JSONResponse(serializer.data)

def get_instructors(request):
    if 'subject' not in request.GET:
        return JSONResponse({'error': 'Must include subject parameter'})
    subject = Subject.objects.get(symbol=request.GET.get('subject'))
    instructors = Instructor.objects.filter(subjects__symbol=request.GET.get('subject'))
    serializer = TermSerializer(instructors, many=True)
    return JSONResponse(serializer.data)

def get_courses(request):
    if 'class_num' in request.GET:
        courses = Course.objects.filter(class_num__in=request.GET.getlist('class_num'))
    elif 'term' in request.GET and 'subject' in request.GET:
        term = Term.objects.get(term_id=request.GET.get('term'))
        courses = Course.objects.filter(term=term, subject=request.GET.get('subject'))
    elif 'term' in request.GET and 'instructor' in request.GET:
        term = Term.objects.get(term_id=request.GET.get('term'))
        try:
            instructor = Instructor.objects.get(name=request.GET.get('instructor'))
        except Instructor.DoesNotExist:
            return JSONResponse({'error': 'We could not find that instructor.'})
        courses = Course.objects.filter(term=term, instructor=instructor)
    else:
        return JSONResponse({'error': 'Must include specific class_nums, or the term and the subject parameters.'})

    serializer = CourseSerializer(courses, many=True)
    return JSONResponse(serializer.data)

