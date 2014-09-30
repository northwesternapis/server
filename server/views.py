import datetime
import random
import string
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
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


# Helpers
# =======

# If users try to access the root URL, send them to the
# documentation
def landing_page(request):
    return redirect('http://developer.asg.northwestern.edu')

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# These need to be freshly generated
INVALID_KEY = lambda: JSONResponse({'error': 'Invalid or missing API key'})
OVER_LIMIT = lambda: JSONResponse({'error': 'You have reached your limit of API requests for the day'})
INVALID_PARAMS = lambda: JSONResponse({'error': 'One or more parameters was invalid'})
PARAM_FAIL = lambda: JSONResponse({'error': 'Invalid combination of parameters'})


def check_key(view):
    def checked_view(*args, **kwargs):
        request = args[0]
        key = request.GET.get('key')
        try:
            project = APIProject.objects.get(api_key=key)
        except APIProject.DoesNotExist:
            return INVALID_KEY()
        if project.requests_sent < project.daily_limit:
            project.requests_sent += 1
            project.save()
        else:
            return OVER_LIMIT()
        return view(*args, **kwargs)
    return checked_view



# Terms and schools
# =================
# These two endpoints have no filtering parameters

@check_key
def get_terms(request):
    terms = Term.objects.filter(
                    shopping_cart_date__lt=datetime.date.today())\
                .order_by('-term_id')
    serializer = TermSerializer(terms, many=True)
    return JSONResponse(serializer.data)

@check_key
def get_schools(request):
    schools = School.objects.all().order_by('symbol')
    serializer = SchoolSerializer(schools, many=True)
    return JSONResponse(serializer.data)


# Subjects and instructors
# ========================

@check_key
def get_subjects(request):
    subjects = Subject.objects
    for param in request.GET:
        if param == 'term':
            subjects = subjects.filter(term__term_id=request.GET['term'])
        elif param == 'school':
            subjects = subjects.filter(school__symbol=request.GET['school'])
    subjects = subjects.order_by('symbol', 'name')\
                       .distinct('symbol', 'name')\
                       .values('symbol', 'name')
    serializer = SubjectSerializer(subjects, many=True)
    return JSONResponse(serializer.data)

@check_key
def get_instructors(request):
    if 'subject' not in request.GET:
        return JSONResponse({'error': 'Must include subject parameter'})
    # Don't return the one null instructor that has all subjects
    instructors = Instructor.objects.filter(
                        subjects__symbol=request.GET.get('subject'))\
                    .exclude(id=1)
    serializer = InstructorSerializer(instructors, many=True)
    return JSONResponse(serializer.data)


# TODO add endpoint for course search, more limited no of queries
@check_key
def search_courses(request):
    # Search by term, subject, and number
    params = request.GET
    if 'term' in params and 'subject' in params and 'catalog_num' in params:
        # term should be an integer
        term = int(params['term'])

        # subject should be at least the first four letters of a subject
        subject = params['subject']
        if len(subject) < 4:
            return INVALID_PARAMS()

        # catalog number should be at least the first character of a course number
        catalog_num = params['catalog_num']
        if len(catalog_num) < 1:
            return INVALID_PARAMS()

        result = Course.objects.filter(term__term_id=term,
                                       subject__istartswith=subject,
                                       catalog_num__startswith=catalog_num)

    elif 'term' in params and 'instructor' in params:
        # term should be an integer
        term = int(params['term'])
        
        # instructor should be an integer representing the id of a prof
        instructor = int(params['instructor'])

        result = Course.objects.filter(term__term_id=term,
                                       instructor=instructor)

        # optional: subject
        if 'subject' in params:
            subject = params['subject']
            if len(subject) < 4:
                return INVALID_PARAMS()
            result = result.filter(subject__istartswith=subject)

        # optional: catalog number
        if 'catalog_num' in params:
            catalog_num = params['catalog_num']
            if len(catalog_num) < 1:
                return INVALID_PARAMS()
            result = result.filter(catalog_num__startswith=catalog_num)

    elif 'term' in params and 'title_query' in params:
        # term should be an integer
        term = int(params['term'])

        # title query is a word or continuous string that 
        # should be in the title of the course
        title_query = params['title_query']

        result = Course.objects.filter(term__term_id=term,
                                       title__icontains=title_query)

        # optional: instructor, id of the instructor
        if 'instructor' in params:
            instructor = int(params['instructor'])
            result = result.filter(instructor=instructor)

    else:
        return PARAM_FAIL()

    # Search by term and professor
    # number optional
    serializer = CourseSummarySerializer(result.order_by('catalog_num'),
                                         many=True)
    return JSONResponse(serializer.data)





# Courses
# =======

def validate_course_search_params(params):
    if 'instructor' in params:
        return True
    if 'id' in params:
        return True
    if 'term' in params:
        return 'room' in params or\
               'subject' in params
    return False

# Normal filtering parameters
allowed_params = set(['subject', 'catalog_num', 'meeting_days',
                      'component', 'section'])
int_params = set(['id', 'term', 'instructor', 'room', 'seats',
                  'class_num', 'course_id'])
allowed_params.update(int_params)

# Parameters which can optionally have a __lt, __gt
# __lte, or __gte suffix
exts = ['__lt', '__gt', '__lte', '__gte']
time_params = set(['start_time', 'end_time'])
date_params = set(['start_date', 'end_date'])
special_params = time_params | date_params | set(['seats'])
allowed_params.update(special_params)
allowed_params.update(param + ext\
                      for ext in exts\
                      for param in special_params)

# Limit number of courses users can query by id,
# to prevent someone from requesting all courses
ID_LIMIT = 200

def filter_courses(params):
    courses = Course.objects

    print params
    try:
        for param in params:
            if param in allowed_params:
                if param == 'id':
                    value = params.getlist(param)[:ID_LIMIT]
                elif param in int_params:
                    value = int(params[param])
                elif param in time_params:
                    value = datetime.datetime.strptime(params[param],
                                '%H:%M').time()
                elif param in date_params:
                    value = datetime.datetime.strptime(params[param],
                                '%Y-%m-%d').date()
                else:
                    value = params[param]

                # Special cases - term is filtered by attr on that model
                if param == 'term':
                    courses = courses.filter(term__term_id=value)
                elif param == 'id':
                    # allow multiple ids
                    courses = courses.filter(id__in=value)
                elif param == 'room_id':
                    courses = courses.filter(room__id=value)
                else:
                    courses = courses.filter(**{param: value})
    except:
        return False

    return courses

@check_key
def get_courses(request):
    if not validate_course_search_params(request.GET):
        return PARAM_FAIL()
    courses = filter_courses(request.GET)
    if courses == False:
        return INVALID_PARAMS()
    serializer = CourseSummarySerializer(courses.order_by('catalog_num'),
                                         many=True)
    return JSONResponse(serializer.data)

@check_key
def get_courses_with_details(request):
    if not validate_course_search_params(request.GET):
        return PARAM_FAIL()
    courses = filter_courses(request.GET)
    serializer = CourseSerializer(courses.order_by('catalog_num'), many=True)
    return JSONResponse(serializer.data)



# Buildings and rooms
# ===================

geo_params = ['lon', 'lat']
geo_filters = set(param + ext for param in geo_params for ext in exts)

@check_key
def get_buildings(request):
    buildings = Building.objects
    for param in request.GET:
        if param == 'id':
            buildings = buildings.filter(id__in=request.GET.getlist('id'))
        elif param in geo_filters:
            value = float(request.GET[param])
            buildings = buildings.filter(**{param: value})
    serializer = BuildingSerializer(buildings.order_by('name'), many=True)
    return JSONResponse(serializer.data)


def filter_rooms(params):
    if 'building' in params:
        building = Building.objects.get(id=int(params['building']))
        return Room.objects.filter(building=building)
    elif 'id' in params:
        return Room.objects.filter(id__in=params.getlist('id'))
    return False

@check_key
def get_rooms(request):
    rooms = filter_rooms(request.GET)
    if rooms == False:
        return INVALID_PARAMS()
    serializer = RoomSerializer(rooms, many=True)
    return JSONResponse(serializer.data)

@check_key
def get_rooms_with_details(request):
    rooms = filter_rooms(request.GET)
    if rooms == False:
        return INVALID_PARAMS()
    serializer = RoomDetailsSerializer(rooms, many=True)
    return JSONResponse(serializer.data)



# API key management pages
# ========================


def login_user(request):
    # redirect user if he/she is already logged in
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Admins').count() == 1:
            return redirect('/manage/approve/')
        return redirect(settings.LOGIN_REDIRECT_URL)

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
        if request.user.is_authenticated()\
                and request.user.groups.filter(name='Admins').count() == 1:
            return fn(request)
        return HttpResponseForbidden('HTTP 403 Not Permitted')
    return _fn


# For Ann and Jaci to approve/manage API key requests
@limit_to_admins
def manage_approvals(request):
    pending = APIProjectRequest.objects.filter(status='S')\
                                       .order_by('date_submitted')
    projects = APIProject.objects.filter(is_active=True)\
                                 .order_by('-date_approved')
    if 'approved' in request.GET:
        message = 'Project succesfully approved'
    elif 'rejected' in request.GET:
        message = 'Project rejected'
    return render(request, 'manage_approvals.html', locals())

@limit_to_admins
def approve_or_reject_project(request):
    project_request = APIProjectRequest.objects\
                            .get(id=int(request.GET['id']))
    if request.GET['action'] == 'approve':
        project_request.status = 'A'
        project_request.save()

        # Generate a new API key
        new_key = ''.join(random.choice(string.ascii_letters\
                            + string.digits) for i in xrange(16))

        # Create the APIProject object
        project = APIProject()
        project.owner = project_request.owner
        project.name = project_request.name
        project.api_key = new_key
        project.original_request = project_request
        project.approved_by = request.user
        project.save()

        # Send e-mail notification
        send_mail('Northwestern Course Data API Project Approved',
                  'Good news: {0} has approved your project named {1}! \nAccess your new API key at http://api.asg.northwestern.edu/manage/projects/'\
                      .format(project.approved_by.get_full_name(), project.name), 
                  'Northwestern Course Data API <noreply@api.asg.northwestern.edu>', 
                  [project_request.owner.email], fail_silently=True)

    elif request.GET['action'] == 'reject':
        project_request.status = 'R'
        project_request.save()
    return redirect('/manage/approve/')

@limit_to_admins
def inactive_projects(request):
    inactive_projects = APIProject.objects.filter(is_active=False)
    return render(request, 'inactive_projects.html', locals())

# For a logged-in user to look at his/her projects
@login_required
def view_projects(request):
    if 'success' in request.GET:
        message = 'Project request successfully submitted.'
    elif 'addreferrer' in request.GET:
        message = 'Allowed referrer added.'
    elif 'deletereferrer' in request.GET:
        message = 'Allowed referrer deleted.'
    pending_requests = APIProjectRequest.objects.filter(owner=request.user,
                                                        status='S')
    projects = APIProject.objects.filter(is_active=True, owner=request.user)
    return render_to_response('view_projects.html', locals(),
                context_instance=RequestContext(request))

@login_required
def new_project(request):
    errors = []
    if APIProjectRequest.objects.filter(owner=request.user, status='S')\
                                .count() >= 2:
        errors.append('You\'ve already submitted two requests that are pending approval. Wait until they\'ve been reviewed to submit more projects.')
    elif request.method == 'POST':
        if 'terms_agreement' in request.POST:
            combined = dict(request.POST.items()\
                                + {'owner': request.user.id}.items())
            project_request = APIProjectRequestForm(combined)
            if project_request.is_valid():
                # If no errors, create the project request object
                c = APIProjectRequest.objects.create(\
                                        **project_request.cleaned_data)
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

@login_required
def edit_referrer(request):
    action = request.POST.get('action')
    project = APIProject.objects.get(id=int(request.POST.get('project')))
    if action == 'add':
        if AllowedReferrer.objects.filter(project=project).count() < 3:
            referrer, added = AllowedReferrer.objects.get_or_create(
                project=project,
                url=request.POST.get('domain'))
            if added:
                return redirect('/manage/projects/?addreferrer')
    elif action == 'delete':
        try:
            url = request.POST.get('referrer_url')
            AllowedReferrer.objects.get(project=project, url=url).delete()
            return redirect('/manage/projects/?deletereferrer')
        except AllowedReferrer.DoesNotExist:
            pass
    return redirect('/manage/projects/')
