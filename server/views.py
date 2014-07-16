import datetime
import random
import string
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from server.forms import *
from server.models import *
from server.serializers import *


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
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
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



def limit_to_admins(fn):
    def _fn(request):
        if request.user.is_authenticated() and request.user.groups.filter(name='Admins').count() == 1:
            return fn(request)
        raise Http404
    return _fn

# For Ann and Jaci to approve/manage API key requests
#@limit_to_admins
def manage_approvals(request):
    pending = APIProjectRequest.objects.filter(status='S').order_by('date_submitted')
    projects = APIProject.objects.filter(is_active=True).order_by('-date_approved')
    if 'approved' in request.GET:
        message = 'Project succesfully approved'
    elif 'rejected' in request.GET:
        message = 'Project rejected'
    return render(request, 'manage_approvals.html', locals())

#@limit_to_admins
def approve_or_reject_project(request):
    project_request = APIProjectRequest.objects.get(id=int(request.GET['id']))
    if request.GET['action'] == 'approve':
        project_request.status = 'A'
        project_request.save()

        # Generate a new API key
        new_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in xrange(16))

        # Create the APIProject object
        project = APIProject()
        project.owner = project_request.owner
        project.name = project_request.name
        project.api_key = new_key
        project.original_request = project_request
        project.approved_by = request.user
        project.save()

    elif request.GET['action'] == 'reject':
        project_request.status = 'R'
        project_request.save()
    return redirect('/manage/approve/')

#@limit_to_admins
def inactive_projects(request):
    inactive_projects = APIProject.objects.filter(is_active=False)
    return render(request, 'inactive_projects.html', locals())

# For a logged-in user to look at his/her projects
#@login_required
def view_projects(request):
    if 'success' in request.GET:
        message = 'Project request successfully submitted.'
    pending_requests = APIProjectRequest.objects.filter(owner=request.user, status='S')
    projects = APIProject.objects.filter(is_active=True, owner=request.user)
    return render_to_response('view_projects.html', locals(),
                context_instance=RequestContext(request))

#@login_required
def new_project(request):
    errors = []
    if APIProjectRequest.objects.filter(owner=request.user, status='S').count() >= 2:
        errors.append('You\'ve already submitted two requests that are pending approval. Wait until they\'ve been reviewed to submit more projects.')
    elif request.method == 'POST':
        if 'terms_agreement' in request.POST:
            combined = dict(request.POST.items() + {'owner': request.user.id}.items())
            project_request = APIProjectRequestForm(combined)
            if project_request.is_valid():
                # If no errors, create the project request object
                c = APIProjectRequest.objects.create(**project_request.cleaned_data)
                return redirect('/manage/projects/?success')
            else:
                fields = project_request.cleaned_data
                if 'name' not in fields:
                    errors.append('You must state the name of your project')
                if 'description' not in fields:
                    errors.append('You must include a description of your project')
                if 'how_long' not in fields:
                    errors.append('You must state how long you will need access')
        else:
            errors.append('You must agree to the Terms of Use in order to apply for an API key.')

    return render(request, 'new_project.html', locals())




# If users try to access the root URL, send them to the
# documentation
def landing_page(request):
    return redirect('http://developer.asg.northwestern.edu')
