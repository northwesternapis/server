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
    schools = School.objects.all().order_by('symbol')
    serializer = SchoolSerializer(schools, many=True)
    return JSONResponse(serializer.data)

def get_terms(request):
    terms = Term.objects.filter(shopping_cart_date__lt=datetime.date.today()).order_by('-term_id')
    serializer = TermSerializer(terms, many=True)
    return JSONResponse(serializer.data)

def get_instructors(request):
    if 'subject' not in request.GET:
        return JSONResponse({'error': 'Must include subject parameter'})
    # Don't return the one null instructor that has all subjects
    instructors = Instructor.objects.filter(subjects__symbol=request.GET.get('subject'))\
                                                                    .exclude(id=1)
    serializer = InstructorSerializer(instructors, many=True)
    return JSONResponse(serializer.data)

# helper
def filter_courses(request):
    if 'term' in request.GET and 'subject' in request.GET:
        term = Term.objects.get(term_id=request.GET.get('term'))

        # If there's an exact match for the subject, return that
        # otherwise if the parameter is four or more letters,
        # get courses with subjects that start with the parameter
        subject = request.GET.get('subject')
        courses = Course.objects.filter(term=term, subject=subject)
        if courses.count() == 0 and len(subject) > 3:
            courses = Course.objects.filter(term=term, subject__istartswith=subject)
    elif 'instructor' in request.GET:
        try:
            instructor = Instructor.objects.get(id=request.GET.get('instructor'))
        except Instructor.DoesNotExist:
            return (JSONResponse({'error': 'We could not find that instructor.'}), False)
        courses = Course.objects.filter(instructor=instructor)
        if 'term' in request.GET:
            courses = courses.filter(term__term_id=request.GET.get('term'))
    elif 'class_num' in request.GET:
        courses = Course.objects.filter(class_num__in=request.GET.getlist('class_num'))
        if 'term' in request.GET:
            term = Term.objects.get(term_id=request.GET.get('term'))
            courses = courses.filter(term=term)
        if 'course_id' in request.GET:
            courses = courses.filter(course_id__in=request.GET.getlist('course_id'))
    elif 'id' in request.GET:
        courses = Course.objects.filter(id__in=request.GET.getlist('id'))
    else:
        return (JSONResponse({'error': 'Must include specific class_nums, or the term and the subject parameters.'}), False)

    return (courses, True)


def get_courses(request):
    result, success = filter_courses(request)
    if not success:
        return result
    serializer = CourseSerializer(result.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)

def get_courses_summary(request):
    result, success = filter_courses(request)
    if not success:
        return result
    serializer = CourseSummarySerializer(result.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)

