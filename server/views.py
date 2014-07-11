import datetime
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from server.serializers import *
from server.models import *


# =============
# API endpoints
# =============

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
        return (JSONResponse({'error': 'An invalid combination of parameters was received.'}), False)

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


param_fail = JSONResponse({'error': 'One or more parameters was invalid'})
fail = JSONResponse({'error': 'Invalid combination of parameters'})

def search_courses(request):
    # Search by term, subject, and number
    params = request.GET
    if 'term' in params and 'subject' in params and 'catalog_num' in params:
        # term should be an integer
        term = int(params['term'])

        # subject should be at least the first four letters of a subject
        subject = params['subject']
        if len(subject) < 4:
            return param_fail

        # catalog number should be at least the first character of a course number
        catalog_num = params['catalog_num']
        if len(catalog_num) < 1:
            return param_fail

        result = Course.objects.filter(term__term_id=term, subject__istartswith=subject, catalog_num__startswith=catalog_num)

    elif 'term' in params and 'instructor' in params:
        # term should be an integer
        term = int(params['term'])
        
        # instructor should be an integer representing the id of a prof
        instructor = int(params['instructor'])

        result = Course.objects.filter(term__term_id=term, instructor=instructor)

        # optional: subject
        if 'subject' in params:
            subject = params['subject']
            if len(subject) < 4:
                return param_fail
            result = result.filter(subject__istartswith=subject)

        # optional: catalog number
        if 'catalog_num' in params:
            catalog_num = params['catalog_num']
            if len(catalog_num) < 1:
                return param_fail
            result = result.filter(catalog_num__startswith=catalog_num)

    elif 'term' in params and 'title_query' in params:
        # term should be an integer
        term = int(params['term'])

        # title query is a word or continuous string that 
        # should be in the title of the course
        title_query = params['title_query']

        result = Course.objects.filter(term__term_id=term, title__icontains=title_query)

        # optional: instructor, id of the instructor
        if 'instructor' in params:
            instructor = int(params['instructor'])
            result = result.filter(instructor=instructor)

    else:
        return fail

    # Search by term and professor
    # number optional
    serializer = CourseSummarySerializer(result.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)





# Courses
# =======

def validate_course_search_params(params):
    if not('id' in params or 'instructor' in params or 'term' in params):
        return False
    if 'term' in params:
        is_valid = 'instructor' in params or\
                   'room' in params or\
                   'subject' in params or\
                   'course_num' in params or\
                   'component' in params
                   # TODO
        return is_valid
    return True

def TEMPfilter_courses(params):
    courses = Course.objects

    return courses

def TEMPget_courses(request):
    if not validate_course_search_params(request.GET):
        return fail
    courses = filter_courses(request.GET)
    serializer = CourseSummarySerializer(result.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)

def TEMPget_courses_detail(request):
    if not validate_course_search_params(request.GET):
        return fail
    serializer = CourseSerializer(result.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)



# API key management pages
# ========================


def login_user(request):
    errors = []
    if request.method == 'POST':
        user = authenticate(username=request.POST['netid'],
                            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.groups.filter(name='Admins').count() == 1:
                    return redirect('/manage/approve/')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                errors.append('There is a problem with your account')
        else:
            errors.append('Incorrect username or password')
    return render(request, 'login.html', locals())

def logout_user(request):
    logout(request)
    return redirect('/manage/login/')


@login_required
def new_project(request):
    return render(request, 'new_project.html', locals())


def limit_to_admins(fn):
    def _fn(request):
        if request.user.is_authenticated() and request.user.groups.filter(name='Admins').count() == 1:
            return fn(request)
        raise Http404
    return _fn

# For Ann and Jaci to approve/manage API key requests
@limit_to_admins
def manage_approvals(request):
    return render(request, 'manage_approvals.html', locals())

# For a logged-in user to look at his/her projects
@login_required
def view_projects(request):
    return render_to_response('view_projects.html', locals(),
                context_instance=RequestContext(request))






# Documentation pages
# ===================

def landing_page(request):
    return render_to_response('landing_page.html')
