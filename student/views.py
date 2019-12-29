import csv

from django.views import generic

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import render, get_list_or_404, get_object_or_404

from django.urls import reverse_lazy

from django.contrib import messages
from django.http import HttpResponse

from .models import Subject_Profile, FacultySubject, Student, Faculty, Marklist, ClassAttendanceMap
from django.contrib.auth.models import User
# for user forms (4 imports)
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import Userform

from tablib import Dataset
from .resources import StudentResource

from django.contrib.auth.decorators import login_required, user_passes_test  # for custom views only

from django.utils.decorators import method_decorator  # for CBV

from .forms import StudentCsvForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import logging

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .models import CustomUser

from django.core.mail import send_mail
from django.conf import settings

import logging

logging.config.dictConfig({

    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'debug_file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'

        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'debug_file',
            #'filename' : '/home/csadmin/waise2/env/logs/django_debug.log'
            'filename': '../env/logs/django_debug.log'
        },

        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'debug_file',
            # 'filename' : '/home/csadmin/waise2/env/logs/django_debug.log'
            'filename': '../env/logs/django_debug.log'

        },
    },

    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['debug_file', ]
        },

        'a': {
            'level': 'ERROR',
            'handlers': ['error_file', ]
        }
    }
})

logger = logging.getLogger(__name__)


# import PySMS
#
# def sms(request):
#
#     ps=PySMS.PySMS(address="",password="",smtp_server="",smtp_port="",ssl=True)
#
#     ps.add_number(number="")
#
#     ps.text("Welcome to Waise ") 
# from .models import Attendence


def attendence_calc(request, regno, section, cursem, id):
    # def attendence_list_pdf(request):/
    logger.info('URL %s calls attendence_calc ', request.get_full_path())
    logger.info('username %s ', request.user.username)
    if request.method == 'GET':
        branch = request.user.dept

        cursem = cursem
        section = section
        # facultyid = facultyid
        # subcode = request.GET['subcode']

        list = RollnoRegnoMap.objects.filter(branch=branch, cursem=cursem, section=section, id=id).order_by('regno', )

        names = []

        for student in list:
            names.append(student.name)

        print("naems are ", names)
        print("list ", list)
        list2 = []

        # list2 = RollnoRegnoMap.objects.filter(bra)
        # print("len list ", len(list))
        # print("zxzx1 ",list[0].name)
        # print("zczcszxzx1 ", list[1].name)
        total = []
        present_total = []
        absent_total = []
        ptotal = 0
        atotal = 0
        prev_atotal = 0
        prev_ptotal = 0
        prev_name = ""

        # student.ptotal=0 
        for student in list:
            if student.atotal == -1:
                atotal = 0

            if student.ptotal == -1:
                ptotal = 0

            if prev_name == student.name:
                atotal = prev_atotal
                ptotal = prev_ptotal
            else:
                atotal = 0
                ptotal = 0

            if student.firsthr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.secondhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.thirdhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.fourthhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.fifthhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.sixthhr == "P":
                ptotal = ptotal + 1

            present_total.append(ptotal)

            if student.firsthr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.secondhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.thirdhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.fourthhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.fifthhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.sixthhr == "A":
                atotal = atotal + 1

            prev_name = student.name
            prev_ptotal = ptotal
            prev_atotal = atotal
            absent_total.append(atotal)
            total.append(atotal + ptotal)
            # print("id ",student.id) 
            RollnoRegnoMap.objects.filter(id=student.id, branch=branch, cursem=cursem, section=section).update(
                atotal=atotal, ptotal=ptotal, )

            # obj,created = Attendence.objects.update_or_create().filter()

        print("p ", ptotal)
        print("a ", atotal)
        print(present_total)
        print(absent_total)
        print("total ", total)

        context = {'list': list,
                   'year': list[0].year,
                   'end_year': list[0].year + 4,
                   # 'facultyid': facultyid,
                   # 'subcode': subcode,
                   'cursem': cursem,
                   'branch': branch,
                   'section': section,
                   'present_total': present_total,
                   'absent_total': absent_total,
                   'total': total,
                   }

        return render(request, 'student/attendence_pdf_view.html', context)

        # html_string = render_to_string('student/attendence_pdf_view.html', context)
        # html = HTML(string=html_string)
        # doc = html.render()
        # pdf = doc.write_pdf()
        # pdf['Content-Disposition']='inline filename:attendem.pdf'
        # pdf['Content-Disposition'] = 'attachment filename:attendence.pdf'
        # return HttpResponse(pdf, content_type='application/pdf')


def email(request):
    subject = 'Welcome user '
    message = 'Thank you for registering to our site '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['swamysneduvelil@gmail.com']

    send_mail(subject, message, email_from, recipient_list, fail_silently=True)
    return redirect("student:home")


#
# from googlevoice import Voice
# from googlevoice.util import input
# def sms(request):
#     username = settings.EMAIL_HOST_USER
#     password = settings.EMAIL_HOST_PASSWORD
#
#     voice=Voice()
#     voice.login(username,password)
#     voice.send_sms("+918547485481",'Hello swamys')


def t(request):
    html_string = render_to_string('student/marklist_pdf_view.html', context)
    html = HTML(string=html_string)
    doc = html.render()
    pdf = doc.write_pdf()
    pdf['Content-Disposition'] = 'inline filename:attendence.pdf'
    return HttpResponse(pdf, content_type='application/pdf')

    # return render(request,'student/attendence_pdf_view.html') 


def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline filename="marklist.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, 'Hello World')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required()
def StudentCsv(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        data = {}

        if "GET" == request.method:
            return render(request, "student/studentcsv.html", data)
            # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            logger.info('URL %s calls StudentCsv ', request.get_full_path())
            logger.info('username %s ', request.user.username)
            if not csv_file.name.endswith('.csv'):
                logger.error('File is not CSV type %s', request.FILES["csv_file"])
                return HttpResponseRedirect(reverse("student:student_addcsv"))
                # if file is too large, return
            if csv_file.multiple_chunks():
                logger.error("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                logger.error("filename %s ", request.FILES["csv_file"])
                return HttpResponseRedirect(reverse("student:student_addcsv"))

            data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for data_dict in data:

                try:
                    form = StudentCsvForm(data_dict)
                    # print("-----------", data_dict)
                    if form.is_valid():
                        form.save()
                    else:
                        logger.error(form.errors.as_json())
                        lst=[]
                        for i in form.errors:
                            lst.append(str((i,form.errors[i])))
                        return render(request,"student/faculty_attendance_main.html",{'obj':lst})
                except Exception as e:
                    logger.error(repr(e))
                    pass

        except Exception as e:
            logger.error("Unable to upload file. " + repr(e))
            logger.error("filename %s ", request.FILES["csv_file"])

        return HttpResponseRedirect(reverse("student:index"))

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .forms import MarklistCsvform


@login_required()
def MarklistCsv(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        data = {}

        if "GET" == request.method:
            return render(request, "student/marklistcsv.html", data)
            # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            logger.info("URL %s calls MarklistCsv ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            if not csv_file.name.endswith('.csv'):
                logger.error("File is not CSV type %s", request.FILES['csv_file'])
                return HttpResponseRedirect(reverse("student:student_addcsv"))
                # if file is too large, return
            if csv_file.multiple_chunks():
                logger.error("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                logger.error("filename %s ", request.FILES["csv_file"])
                return HttpResponseRedirect(reverse("student:student_addcsv"))

            file_data = csv_file.read().decode("utf-8")
            # print("file data ", file_data)

            lines = file_data.split("\n")
            # print("lines ", lines)
            lines.pop()

            # loop over the lines and save them in db. If error , store as string and then display
            firstline = True
            data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for data_dict in data:
                try:
                    form = MarklistCsvform(data_dict)
                    print("csv data", data_dict)
                    # print("modelform ",form)
                    if form.is_valid():
                        form.save()
                    else:
                        logger.error(form.errors.as_json())
                        lst = []
                        for i in form.errors:
                            lst.append(str((i, form.errors[i])))
                        return render(request, "student/faculty_attendance_main.html", {'obj': lst})
                except Exception as e:
                    logger.error(repr(e))
                    pass

        except Exception as e:
            logger.error("Unable to upload file. " + repr(e))
            logger.error("filename %s ", request.FILES["csv_file"])

        return HttpResponseRedirect(reverse("student:index"))

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .forms import AttendenceCsvForm


@login_required()
def AttendenceCsv(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        data = {}

        if "GET" == request.method:
            return render(request, "student/attendencecsv.html", data)
            # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            logger.info("URL %s calls AttendenceCsv ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            if not csv_file.name.endswith('.csv'):
                logger.error('File is not CSV type %s', request.FILES["csv_file"])
                return HttpResponseRedirect(reverse("student:student_addcsv"))
                # if file is too large, return
            if csv_file.multiple_chunks():
                logger.error("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                logger.error("filename %s ", request.FILES['csv_file'])
                return HttpResponseRedirect(reverse("student:student_addcsv"))

            data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for data_dict in data:
                    # data_dict[""]
                    try:
                        form = AttendenceCsvForm(data_dict)
                        # print("-----------", data_dict)
                        if form.is_valid():
                            form.save()
                        else:
                            logger.error(form.errors.as_json())
                            lst = []
                            for i in form.errors:
                                lst.append(str((i, form.errors[i])))
                            return render(request, "student/faculty_attendance_main.html", {'obj': lst})
                    except Exception as e:
                        logger.error(repr(e))
                        pass

        except Exception as e:
            logger.error("Unable to upload file. " + repr(e))
            logger.error("filename %s ", request.FILES['csv_file'])

        return HttpResponseRedirect(reverse("student:index"))

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .filters import StudentDetailFilter

# @login_required()

from django.template.loader import render_to_string, get_template
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML


def render_to_pdf(request):
    if request.method == 'GET':
        if 'regno' in request.GET or 'cursem' in request.GET or 'branch' in request.GET:
            regno = request.GET['regno']
            cursem = request.GET['cursem']
            branch = request.GET['branch']
            logger.info("URL %s calls render_to_pdf ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            # print("++++++++++++++", request.GET)

            list = get_list_or_404(Student, pk=regno)
            marklist = get_list_or_404(Marklist, regno=regno, branch=branch, cursem=cursem)
            sub1 = get_object_or_404(Subject_Profile, code=marklist[0].subcode1)

            sub2 = get_object_or_404(Subject_Profile, code=marklist[0].subcode2)
            sub3 = get_object_or_404(Subject_Profile, code=marklist[0].subcode3)
            sub4 = get_object_or_404(Subject_Profile, code=marklist[0].subcode4)

            if marklist[0].subcode5 != 0:

                sub5 = Subject_Profile.objects.filter(code=marklist[0].subcode5)
            else:
                sub5 = "empty"

            if marklist[0].subcode6 != 0:

                sub6 = Subject_Profile.objects.filter(code=marklist[0].subcode6)
            else:
                sub6 = "empty"

            if marklist[0].subcodel3 != 0:

                subl3 = Subject_Profile.objects.filter(code=marklist[0].subcodel3)
            else:
                subl3 = "empty"

            if marklist[0].subcodel4 != 0:

                subl4 = Subject_Profile.objects.filter(code=marklist[0].subcodel4)
            else:
                subl4 = "empty"
            #
            # subl1 = Subject_Profile.objects.filter(code=marklist[1].subcodel1)
            # subl2 = Subject_Profile.objects.filter(code=marklist[1].subcodel2)
            #
            # subl3 = Subject_Profile.objects.filter(code=marklist[1].subcodel3)
            # subl4 = Subject_Profile.objects.filter(code=marklist[1].subcodel4)
            # sub5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # sub6 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            subl1 = get_object_or_404(Subject_Profile, code=marklist[1].subcodel1)
            subl2 = get_object_or_404(Subject_Profile, code=marklist[1].subcodel2)
            # subl3 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # subl4 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # subl5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            #
            # print("ffffffffffffffffsubcode5 ", marklist[0].subcode5)
            # print("ffffffffffffffffsub5 ", sub5[0].name)
            #
            # print("ffffffffffffffffsubcode6 ", marklist[0].subcode6)
            # print("ffffffffffffffffsub6 ", sub6)
            #
            # print("ffffffffffffffffsubcodeL3 ", marklist[0].subcodel3)
            # print("ffffffffffffffffsubL3 ", subl3)
            #
            # print("ffffffffffffffffsubcodeL4 ", marklist[0].subcodel4)
            # print("ffffffffffffffffsubL4 ", subl4)

            context = {'list': list,
                       'marks': marklist,
                       'sub1': sub1,
                       'sub2': sub2,
                       'sub3': sub3,
                       'sub4': sub4,
                       'sub5': sub5,
                       'sub6': sub6,
                       'subl1': subl1,
                       'subl2': subl2,
                       'subl3': subl3,
                       'subl4': subl4,
                       'template': 'marklist_pdf_view.html',
                       }

            html_string = render_to_string('student/marklist_pdf_view.html', context)
            html = HTML(string=html_string)
            doc = html.render()
            pdf = doc.write_pdf()
            # pdf['Content-Disposition']='inline filename:marklist.pdf'
            return HttpResponse(pdf, content_type='application/pdf')


def pdf_form(request):
    logger.info("URL %s calls pdf_form ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    return render(request, 'student/pdf_details.html')


def studentdetail_search(request):
    if request.method == 'GET':
        if 'regno' in request.GET or 'cursem' in request.GET or 'branch' in request.GET:
            regno = request.GET['regno']
            cursem = request.GET['cursem']
            branch = request.GET['branch']
            logger.info("URL %s calls studentdetail_search ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            # print("++++++++++++++", request.GET)

            list = get_list_or_404(Student, pk=regno)
            marklist = get_list_or_404(Marklist, regno=regno, branch=branch, cursem=cursem)
            sub1 = get_object_or_404(Subject_Profile, code=marklist[0].subcode1)

            sub2 = get_object_or_404(Subject_Profile, code=marklist[0].subcode2)
            sub3 = get_object_or_404(Subject_Profile, code=marklist[0].subcode3)
            sub4 = get_object_or_404(Subject_Profile, code=marklist[0].subcode4)

            if marklist[0].subcode5 != 0:

                sub5 = Subject_Profile.objects.filter(code=marklist[0].subcode5)
            else:
                sub5 = 0

            if marklist[0].subcode6 != 0:

                sub6 = Subject_Profile.objects.filter(code=marklist[0].subcode6)
            else:
                sub6 = 0

            if marklist[0].subcodel3 != 0:

                subl3 = Subject_Profile.objects.filter(code=marklist[0].subcodel3)
            else:
                subl3 = 0

            if marklist[0].subcodel4 != 0:

                subl4 = Subject_Profile.objects.filter(code=marklist[0].subcodel4)
            else:
                subl4 = 0

            print("sss6 ", marklist[0].subcode6)
            print(" type ", type(marklist[0].subcode6))
            # subl1 = Subject_Profile.objects.filter(code=marklist[1].subcodel1)
            # subl2 = Subject_Profile.objects.filter(code=marklist[1].subcodel2)
            #
            # subl3 = Subject_Profile.objects.filter(code=marklist[1].subcodel3)
            # subl4 = Subject_Profile.objects.filter(code=marklist[1].subcodel4)
            # sub5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # sub6 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            subl1 = get_object_or_404(Subject_Profile, code=marklist[0].subcodel1)
            subl2 = get_object_or_404(Subject_Profile, code=marklist[0].subcodel2)
            # subl3 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # subl4 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
            # subl5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)

            # print("ffffffffffffffffsubcode5 ", marklist[0].subcode5)
            # print("ffffffffffffffffsub5 ", sub5[0].name)
            #
            # print("ffffffffffffffffsubcode6 ", marklist[0].subcode6)
            # print("ffffffffffffffffsub6 ", sub6)
            #
            # print("ffffffffffffffffsubcodeL3 ", marklist[0].subcodel3)
            # print("ffffffffffffffffsubL3 ", subl3)
            #
            # print("ffffffffffffffffsubcodeL4 ", marklist[0].subcodel4)
            # print("ffffffffffffffffsubL4 ", subl4)

            context = {'list': list,
                       'marks': marklist,
                       'sub1': sub1,
                       'sub2': sub2,
                       'sub3': sub3,
                       'sub4': sub4,
                       'sub5': sub5,
                       'sub6': sub6,
                       'subl1': subl1,
                       'subl2': subl2,
                       'subl3': subl3,
                       'subl4': subl4,
                       'template': 'marklist_pdf_view.html',
                       }

            return render(request, 'student/detail.html', context)

    else:
        return render(request, 'student/search_marks_public.html')


def search_form(request):
    if request.user.is_authenticated:
        return render(request, 'student/search_marks_public.html')
    else:
        return render(request, 'student/login.html')


from .forms import UserCsvForm
from django.contrib.auth.hashers import make_password


@login_required()
def UserCsv(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        data = {}

        if "GET" == request.method:
            return render(request, "student/upload_users.html", data)
            # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            logger.info("URL %s calls UserCsv ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            # print("csv file ",csv_file) 
            if not csv_file.name.endswith('.csv'):
                logger.error('File is not CSV type %s ', request.FILES["csv_file"])
                return HttpResponseRedirect(reverse("student:user_csv"))
                # if file is too large, return
            if csv_file.multiple_chunks():
                logger.error("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                logger.error("filename %s ", request.FILES['csv_file'])
                return HttpResponseRedirect(reverse("student:user_csv"))

            file_data = csv_file.read().decode("utf-8")
            # print("file data ", file_data)

            lines = file_data.split("\n")
            # print("lines 1", lines)
            lines.pop()
            # print("lines 2", lines)

            # loop over the lines and save them in db. If error , store as string and then display
            firstline = False

            for line in lines:
                if firstline:
                    firstline = False
                else:
                    fields = line.split(",")
                    # print("fields ", fields)
                    data_dict = {}

                    # print("+++++++++", data_dict)
                    # data_dict["username"]=fields[0]
                    data_dict["first_name"] = fields[0]
                    # data_dict["last_name"] = fields[1]
                    data_dict["username"] = fields[1]
                    password = make_password(fields[2], None, 'pbkdf2_sha256')
                    data_dict["password"] = password
                    data_dict["dept"] = fields[3]
                    data_dict["email"] = fields[4]
                    data_dict["password1"] = password
                    data_dict["password2"] = password

                    try:
                        form = UserCsvForm(data_dict)
                        # print("-----------", data_dict)
                        if form.is_valid():

                            form.save()
                        else:
                            logger.error(form.errors.as_json())
                    except Exception as e:
                        logger.error(repr(e))
                        pass

        except Exception as e:
            logger.error("Unable to upload file. " + repr(e))
            logger.error("filename %s ", request.FILES["csv_file"])

        return HttpResponseRedirect(reverse("student:index"))

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


def UserCreate(request):
    if request.user.groups.filter(name='Dataop').exists() or request.user.groups.filter(
            name='Admin').exists() or request.user.groups.filter(name='HOD'):

        student = UserCsvForm(request.POST or None)
        logger.info("URL %s calls UserCreate ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        # print("form ",student) 
        if student.is_valid():
            instance = student.save(commit=False)
            instance.branch = request.user.dept

            instance.save()

            return render(request, 'student/home.html')

        context = {
            "form": student
        }

        return render(request, 'student/student_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


def home(request):
    if request.user.is_authenticated:
        logger.info("URL %s calls home() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        return render(request, 'student/home.html')
    else:
        return render(request, 'student/login.html')


from django.contrib.auth.models import Group


def loguser(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            uname = request.POST['username']
            passd = request.POST['password']
            logger.info("URL %s calls loguser ", request.get_full_path())
            print('00=============')
            print(CustomUser.objects)
            print('112=============')
            valid_user = CustomUser.objects.filter(username=uname)
            print(valid_user)
            print('11=============')
            if valid_user:
                print('2=============')
                user = authenticate(username=uname, password=passd)
                # user = authenticate(username=user.username, password=user.password)
                # print("dvsdvsv ", valid_user)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        logger.info('%s has logged in ', uname)
                        logger.info('username %s', request.user.username)
                        if user.groups.filter(name='Student'):
                            return HttpResponseRedirect('/student/public_form/')
                        else:
                            return HttpResponseRedirect('/student/home/')
            else:
                print('3==============')
                context = {'error': "Login credentials are invalid"}
                logger.error('%s failed to login ', uname)

                return render(request, 'student/login.html', context)

        print('4=============')
        context = {'error': "Login credentials are invalid"}

        return render(request, 'student/login.html', context)


from django.contrib.auth import login, logout


def logoutuser(request):
    logger.info(" %s logged out", request.user.username)
    logout(request)
    return redirect('/student/')


def testing(request):
    return render(request, 'student/login.html')


class Indexview(generic.ListView):
    template_name = 'student/home.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Student.objects.all()


class DetailView(generic.DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'object_list'


# prints student details
def student_report(request, regno, branch, cursem):
    logger.info("URL %s calls student_report ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    list = get_list_or_404(Student, pk=regno, cursem=cursem)
    marklist = get_list_or_404(Marklist, regno=regno, branch=branch, cursem=cursem)
    sub1 = get_object_or_404(Subject_Profile, code=marklist[0].subcode1)

    sub2 = get_object_or_404(Subject_Profile, code=marklist[0].subcode2)
    sub3 = get_object_or_404(Subject_Profile, code=marklist[0].subcode3)
    sub4 = get_object_or_404(Subject_Profile, code=marklist[0].subcode4)

    # sub1 = Subject_Profile.objects.filter(code=marklist[1].subcode1)
    # sub2 = Subject_Profile.objects.filter(code=marklist[1].subcode2)
    # sub3 = Subject_Profile.objects.filter(code=marklist[1].subcode3)
    # sub4 = Subject_Profile.objects.filter(code=marklist[1].subcode4)
    #
    # print("dvsvvsvv ",marklist[0]) 

    if marklist[0].subcode5 != 0:

        sub5 = Subject_Profile.objects.filter(code=marklist[0].subcode5)
    else:
        sub5 = "empty"

    if marklist[0].subcode6 != 0:

        sub6 = Subject_Profile.objects.filter(code=marklist[0].subcode6)
    else:
        sub6 = "empty"

    if marklist[0].subcodel3 != 0:

        subl3 = Subject_Profile.objects.filter(code=marklist[0].subcodel3)
    else:
        subl3 = "empty"

    if marklist[0].subcodel4 != 0:

        subl4 = Subject_Profile.objects.filter(code=marklist[0].subcodel4)
    else:
        subl4 = "empty"
    #
    # subl1 = Subject_Profile.objects.filter(code=marklist[1].subcodel1)
    # subl2 = Subject_Profile.objects.filter(code=marklist[1].subcodel2)
    #
    # subl3 = Subject_Profile.objects.filter(code=marklist[1].subcodel3)
    # subl4 = Subject_Profile.objects.filter(code=marklist[1].subcodel4)
    # sub5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
    # sub6 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
    subl1 = get_object_or_404(Subject_Profile, code=marklist[1].subcodel1)
    subl2 = get_object_or_404(Subject_Profile, code=marklist[1].subcodel2)
    # subl3 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
    # subl4 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)
    # subl5 = get_object_or_404(Subject_Profile,code=marklist[1].subcode1)

    # print("ffffffffffffffffsubcode5 ", marklist[0].subcode5)
    # print("ffffffffffffffffsub5 ", sub5)
    #
    # print("ffffffffffffffffsubcode6 ", marklist[0].subcode6)
    # print("ffffffffffffffffsub6 ", sub6)
    #
    # print("ffffffffffffffffsubcodeL3 ", marklist[0].subcodel3)
    # print("ffffffffffffffffsubL3 ", subl3)

    # print("ffffffffffffffffsubcodeL4 ", marklist[0].subcodel4)
    # print("ffffffffffffffffsubL4 ", subl4)

    context = {'list': list,
               'marks': marklist,
               'sub1': sub1,
               'sub2': sub2,
               'sub3': sub3,
               'sub4': sub4,
               'sub5': sub5,
               'sub6': sub6,
               'subl1': subl1,
               'subl2': subl2,
               'subl3': subl3,
               'subl4': subl4,
               }
    return render(request, 'student/detail.html', context)


def detail(request, regno):
    logger.info("URL %s calls detail() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    list = get_list_or_404(Student, pk=regno)
    marklist = get_list_or_404(Marklist, regno=regno)

    context = {'list': list,
               'marks': marklist,
               }
    return render(request, 'student/detail.html', context)


@login_required()
def StudentCreate(request):
    if request.user.groups.filter(name='Dataop').exists() or request.user.groups.filter(
            name='Admin').exists() or request.user.groups.filter(name='HOD'):

        student = Studentmodelform(request.POST or None)
        logger.info("URL %s calls StudentCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if student.is_valid():
            instance = student.save(commit=False)
            instance.branch = request.user.dept
            instance.save()

            return render(request, 'student/home.html')

        context = {
            "form": student,
            "title": 'Add Student',
        }

        return render(request, 'student/student_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .forms import Studentupdateform


class Studentdelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student:index')


# form code below


def searchs(request):
    if request.method == 'GET':
        if 'regno' in request.GET or 'name in request.GET' or 'branch in request.GET':
            num = request.GET['regno']
            name = request.GET['name']
            branch = request.GET['branch']
            student = Student.objects.filter(regno__icontains=num, name__icontains=name, branch__icontains=branch)
            students = get_list_or_404(Student, branch__icontains=branch)
            # marks = Marklist.objects.filter(regno_id__icontains=num)
            logger.info("URL %s calls searchs() ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            marks = get_list_or_404(Marklist, regno_id__regno__icontains=num)
            context = {'list': student,
                       'marks': marks,
                       'students': students,
                       }

            message = 'You searched for ', request.GET['regno']

            return render(request, 'student/marklist.html', context)

            # return render(request, 'student/detail.html', context)

        else:
            message = 'You submitted an empty form'

    return HttpResponse(message)


def Studentsearch(request):
    # searchs(request)
    logger.info("URL %s calls Studentsearch() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    return render(request, 'student/search_student.html')


def searchmarks(request):
    if request.method == 'GET' or request.method == 'POST':
        if 'cursem' in request.GET or 'branch' in request.GET or 'section' in request.GET or 'type' in request.GET:
            # num = request.GET['regno']
            # print(request.GET)
            cursem = request.GET['cursem']
            branch = request.user.dept
            section = request.GET['section']
            type = request.GET['type']
            logger.info("URL %s calls searchmarks() ", request.get_full_path())
            logger.info("username %s ", request.user.username)

            print("req dept ", request.user.dept)

            studentformset = modelformset_factory(Marklist, form=StudentForm, extra=0,
                                                  exclude=(
                                                      'id', 'subcode1', 'subcode2', 'subcode3', 'subcode4', 'subcode5',
                                                      'subcode6', 'subcodel1', 'subcodel2', 'subcodel3', 'subcodel4',
                                                      'branch', 'join', 'type'))
            queryset = Marklist.objects.filter(branch=branch, cursem=cursem, type=type).order_by('regno')

            print("post data ", request.POST)
            formset = studentformset(request.POST or None, queryset=queryset)
            print("formset ", formset)

            if len(queryset) != 0:

                # formset.cleaned_data()
                if formset.is_valid():
                    instances = formset.save(commit=False)
                    for instance in instances:
                        # record=instance.cleaned_data()
                        instance.save()

                    return render(request, 'student/marklist_search.html')

                context = {'form': formset,
                           'type': type,
                           'branch': branch,
                           'sem': cursem,
                           'section': section,
                           # 'sub5':sub5,
                           }

                return render(request, 'student/student_marks.html', context)

            else:
                context_error = {
                    'error': 'No data found for given filter'
                }
                return render(request, 'student/marklist_search.html', context_error)


        else:
            message = 'You submitted an empty form'

        return HttpResponse(message)


def Studentform_edit(request, regno):  # working well with register number only

    studentformset = modelformset_factory(Marklist, form=StudentForm, extra=0, fields=(
        'regno', 'cursem', 'section',
        # 'subcode1', 'subcode2', 'subcode3', 'subcode4', 'subcode5', 'subcode6',
        # 'subcodel1',
        # 'subcodel2', 'subcodel3', 'subcodel4',
        'mark1', 'mark2', 'mark3', 'mark4', 'mark5', 'mark6', 'markl1', 'markl2',
        'markl3', 'markl4',))
    queryset = Marklist.objects.filter(regno=regno)
    logger.info("URL %s calls Studentform_edit() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    formset = studentformset(request.POST or None, queryset=queryset)
    # studentformset()
    # print(request.POST)

    # formset.cleaned_data()
    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            # record=instance.cleaned_data()
            instance.save()

    context = {'form': formset
               }

    return render(request, 'student/student_marks.html', context)


def Marklistsearch(request):
    logger.info("URL %s calls Marklistsearch() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    return render(request, 'student/marklist_search.html')


from .forms import StudentForm, Studentmodelform


def Studentform(request):
    # marklist=Marklist.objects.all()
    # regno_id__regno__icontains = num
    marklist = Marklist.filter(regno__icontains=regno)
    logger.info("URL %s calls Studentform() ", request.get_full_path())
    logger.info("username %s ", request.user.username)

    newform = StudentForm(request.POST or None, instance=marklist)
    if newform.is_valid():
        student = newform.save(commit=False)
        student.user = request.user
        student.save()

    context = {'form': newform}
    return render(request, 'student/student_marks.html', context)


from django.forms.models import modelformset_factory, inlineformset_factory

#
# def Studentform_edit(request, regno):  # working well with register number only
#     studentformset = modelformset_factory(Marklist, form=StudentForm, extra=0, fields=(
#         'regno', 'cursem', 'section', 'subcode1', 'subcode2', 'subcode3', 'subcode4', 'subcode5', 'subcode6',
#         'subcodel1',
#         'subcodel2', 'subcodel3', 'subcodel4', 'mark1', 'mark2', 'mark3', 'mark4', 'mark5', 'mark6', 'markl1', 'markl2',
#         'markl3', 'markl4',))
#     queryset = Marklist.objects.filter(regno=regno)
#     formset = studentformset(request.POST or None, queryset=queryset)
#     # studentformset()
#     # print(request.POST)
#
#     # formset.cleaned_data()
#     if formset.is_valid():
#         instances = formset.save(commit=False)
#         for instance in instances:
#             # record=instance.cleaned_data()
#             instance.save()
#
#     context = {'form': formset
#                }
#
#     return render(request, 'student/student_marks.html', context)
#

from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class UserFormView(View):
    form_class = Userform
    template_name = 'student/register_user.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        logger.info("URL %s calls UserFormView() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if form.is_valid():
            user = form.save(commit=False)

            # cleaning the input data from user

            username = form.cleaned_data['username']

            email = form.cleaned_data['email']

            password1 = form.cleaned_data['password1']

            password2 = form.cleaned_data['password2']

            if password1 == password2:
                # accesslvl = form.cleaned_data['accesslvl']

                user.set_password(password1)
                subject = 'User Account Created'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                html_content = render_to_string('student/email_new_user.html', {'username': username})
                text_content = strip_tags(html_content)
                # message = "Welcome to the SOE Student Academic Information System.Your account has been activated. Use the username and the password to login"
                print("sssss   ", text_content)

                user.save()
                mail = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                mail.attach_alternative(html_content, "text/html")
                mail.send(fail_silently=True)

            # to login the user with username and password
            # user = authenticate(username=username, password=password1)
            #
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)

            return redirect('student:home')

        return render(request, self.template_name, {'form': form})
        # context = {'list': user, }
        # return render(request, 'student/account_created.html', context)


from .models import Student, Marklist
from .filters import StudentFilter, MarklistFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required()
def AttendenceUpdate(request, regno, cursem, section, id):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='HOD'):
        instance = get_object_or_404(RollnoRegnoMap, cursem=cursem, section=section, regno=regno, id=id)
        student = RollnoRegnoMapEditForm(request.POST or None, instance=instance)
        logger.info("URL %s calls home() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if student.is_valid():
            instance = student.save(commit=False)
            instance.save()

            return render(request, 'student/home.html')
        context = {
            "form": student,
            "title": "Attendence Update"
        }

        return render(request, 'student/student_form.html', context)


from .filters import AttendenceFilter


#
# @login_required()
# def attendence_search(request):
#     if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
#             name='Admin') or request.user.groups.filter(name='HOD'):
#         if request.method == 'GET':
#             # print("+++++++++++++++++++++++",request.user)
#             student_list = RollnoRegnoMap.objects.filter(branch=request.user.dept).order_by('regno')
#             # page=request.GET.get('page',1)
#             print("req data ",request)
#
#             attendence_filter = AttendenceFilter(request.GET, queryset=student_list)
#
#             # marklist = Marklist.objects.filter(regno=marklist_list)
#
#             # print("+++++++++++++++++++++++ ", attendence_filter)
#
#             return render(request, 'student/rollregnomap_list.html', {'filter': attendence_filter,
#
#                                                                   'title':'Search Attendence',
#                                                                   })
#     else:
#             context = {"perm_error": 'You do not have permission to access this page'}
#
#             return render(request, 'student/login.html', context)
#


@login_required()
def marklist_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='HOD'):

        if request.method == 'GET':
            # print("+++++++++++++++++++++++",request.user)
            # marklist_list = Student.objects.filter(branch=request.user.dept).order_by('regno')
            # page=request.GET.get('page',1)

            # student_filter = StudentFilter(request.GET, queryset=marklist_list)
            logger.info("URL %s calls marklist_search() ", request.get_full_path())
            logger.info("username %s ", request.user.username)

            marklist_list = Marklist.objects.filter(branch=request.user.dept).order_by('regno')

            student_filter = MarklistFilter(request.GET, queryset=marklist_list)

            # marklist = Marklist.objects.filter(regno=marklist_list)

            # print("+++++++++++++++++++++++", student_filter)

            return render(request, 'student/marklist_list.html', {'filter': student_filter,
                                                                  'internal': 'Internal',
                                                                  'external': 'External',
                                                                  'title': 'Search Marklist',
                                                                  })
    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


# @login_required()
@login_required()
def student_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='HOD'):

        if request.method == 'GET':
            # print("+++++++++++++++++++++++",request.user)
            student_list = Student.objects.filter(branch=request.user.dept).order_by('regno')
            # page=request.GET.get('page',1)
            student_filter = StudentFilter(request.GET, queryset=student_list)
            logger.info("URL %s calls student_search() ", request.get_full_path())
            logger.info("username %s ", request.user.username)

            # marklist = Marklist.objects.filter(regno=student_list)

            # print("+++++++++++++++++++++++", student_filter)
            ##marklist =Marklist.objects.all()
            # mark_filter = MarklistFilter(request.GET,queryset=marklist)
            #
            # paginator = Paginator(student_list,2)
            # try:
            #     students=paginator.page(page)
            # except PageNotAnInteger:
            #     students=paginator.page(1)
            # except EmptyPage:
            #     students=paginator.page(paginator.num_pages)

            # print("student ")
            return render(request, 'student/student_list.html', {'filter': student_filter, })
    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


# for faculty only

from .models import Faculty
from .filters import FacultyFilter


@login_required()
def faculty_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):
        faculty_list = Faculty.objects.filter(dept=request.user.dept)
        faculty_filter = FacultyFilter(request.GET, queryset=faculty_list)
        logger.info("URL %s calls faculty_search() ", request.get_full_path())
        logger.info("username %s ", request.user.username)

        context = {
            'filter': faculty_filter,
            'title': 'Search Faculty',
        }

        return render(request, 'student/faculty_list.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .filters import FacultySubjectFilter
from .models import FacultySubject


@login_required()
def facultysubject_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        faculty_list = FacultySubject.objects.all()
        logger.info("URL %s calls facultysubject_search() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        faculty_filter = FacultySubjectFilter(request.GET, queryset=faculty_list)
        context = {'filter': faculty_filter,
                   'title': 'Faculty Subjectmap Search',
                   }
        return render(request, 'student/facultysubject_list.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


class Facultyview(generic.ListView):
    # logger.info("URL %s calls Facultyview() ",request.get_full_path())
    # logger.info("username %s ",request.user.username)
    template_name = 'student/facultyindex.html'
    context_object_name = 'object_list'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Faculty.objects.all()


def FacultyDetail(request, pk):
    logger.info("URL %s calls FacultyDetail() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    list = get_list_or_404(Faculty, pk=pk)

    context = {'list': list,
               'title': 'Faculty Details',
               }
    return render(request, 'student/facultydetail.html', context)


from .forms import Facultymodelform


@login_required()
def FacultyCreate(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):
        faculty = Facultymodelform(request.POST or None)
        logger.info("URL %s calls FacultyCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        # print(faculty)
        if faculty.is_valid():
            instance = faculty.save(commit=False)
            # print(instance.branch)
            instance.dept = request.user.dept
            # print(instance.branch)

            instance.save()
            return render(request, 'student/home.html')

        context = {
            "form": faculty
        }

        return render(request, 'student/faculty_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


#
#
# class FacultyCreate(CreateView):
#     model = Faculty
#     fields = '__all__'
#     success_url = reverse_lazy('student:faculty_show')
# def StudentUpdate(request, pk):
#     if request.user.groups.filter(name='Dataop').exists() or request.user.groups.filter(name='Admin').exists():
#         instance = get_object_or_404(Student, regno=pk)
#         student = Studentupdateform(request.POST or None, instance=instance)
#         if student.is_valid():
#             instance = student.save(commit=False)
#             instance.save()
#
#             return render(request, 'student/home.html')
#         context = {
#             "form": student,
#         }
#
#         return render(request, 'student/student_form.html', context)
#     else:
#         context = {"perm_error": 'You do not have permission to access this page'}
#
#         return render(request, 'student/login.html', context)
#

@login_required()
def Facultyupdate(request, pk):
    if request.user.groups.filter(name='Dataop').exists() or request.user.groups.filter(name='Admin').exists():

        instance = get_object_or_404(Faculty, empid=pk)
        logger.info("URL %s calls Facultyupdate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        print("instance ", instance)
        faculty = Facultymodelform(request.POST or None, request.FILES or None, instance=instance)
        if faculty.is_valid():
            instance = faculty.save(commit=False)
            instance.save()

            return render(request, 'student/home.html')
        context = {
            "form": faculty,
            'title': 'Edit Faculty Details',
        }

        return render(request, 'student/student_form.html', context)
    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)

        # class Facultyupdate(UpdateView):
        #   model = Faculty
        #  fields = '__all__'
        # success_url = reverse_lazy('student:faculty_show')


class Facultydelete(DeleteView):
    model = Faculty
    success_url = reverse_lazy('student:faculty_show')


# for subjects

@login_required()
def SubjectsList(request):
    logger.info("URL %s calls SubjectsList() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    sublist = Subject_Profile.objects.all()
    context = {'list': sublist, }
    return render(request, 'student/subjectdetail.html', context)


# facultysubject map
class FacultySubMapview(generic.ListView):
    template_name = 'student/facultysubmapindex.html'
    context_object_name = 'object_list'

    # logger.info("URL %s calls FacultySubMapview() ",request.get_full_path())
    # logger.info("username %s ",request.user.username)

    def get_queryset(self):
        return FacultySubject.objects.all()


from .forms import FacultySubjectMapAddForm


@login_required()
def FacultySubMapCreate(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='Faculty'):
        submap = FacultySubjectMapAddForm(request.POST or None)
        logger.info("URL %s calls FacultySubMapCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if submap.is_valid():
            instance = submap.save(commit=False)
            # print(instance.branch)
            instance.dept = request.user.dept
            # print(instance.branch)

            instance.save()
            return render(request, 'student/home.html')

        context = {
            "form": submap
        }

        return render(request, 'student/facultysubject_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


@login_required()
@user_passes_test(
    lambda u: u.groups.filter(name='Dataop').exists() or u.groups.filter(name='Faculty').exists() or u.groups.filter(
        name='Admin').exists() or u.groups.filter(name='HOD').exists(), )
class FacultySubMapEdit(UpdateView):
    # logger.info("URL %s calls FacultySubMapEdit() ",request.get_full_path())
    # logger.info("username %s ",request.user.username)
    model = FacultySubject
    fields = '__all__'
    success_url = reverse_lazy('student:faculty_show')


# for marklist

from .models import Marklist

from .forms import MarklistForm


def load_subject_code(request):
    sem_subjects = request.GET.get('cursem')
    branch = request.GET.get('branch')
    # print(request)
    # print(branch)
    # print(sem_subjects)
    sub_code = Subject_Profile.objects.filter(sem=sem_subjects, branch=request.user.dept)
    return render(request, 'student/subname_dropdownlist.html', {'sub_name': sub_code})


def load_subject_name(request):
    # print(request)
    semester = request.GET.get('cursem')
    # subcode= request.GET.get('subcode1')
    # print("vdsvnlk ",subcode, "semes ",semester)
    # print("branch ",request.user.dept)
    sub_name = Subject_Profile.objects.filter(sem=semester, branch=request.user.dept)
    return render(request, 'student/subname.html', {'subname': sub_name})


def load_subject_name2(request):
    # print(request)
    subcode = request.GET.get('subcode2')
    # print("vdsvnlk ",subcode)
    sub_name = Subject_Profile.objects.filter(code=subcode)
    return render(request, 'student/subname.html', {'subname': sub_name})


@login_required()
def MarklistCreate(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='Faculty') or request.user.groups.filter(name='HOD'):

        # queryset=Marklist.objects.filter(branch=request.user.dept)
        # MarklistForm(user=request.user)
        # print("----------------",request.POST)
        logger.info("URL %s calls MarklistCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        marklist = MarklistForm(request.POST or None)
        if marklist.is_valid():
            if request.POST['type'] == 'External':
                # print("**** ", marklist.cleaned_data['mark1'])
                # print("----------", request.POST['mark1'])
                regno = request.POST['regno']
                chance = request.POST['chance']
                cursem = request.POST['cursem']
                branch = request.user.dept

                student_int = Marklist.objects.get(regno=regno, chance=chance, type='Internal', cursem=cursem,
                                                   branch=branch)

                instance = marklist.save(commit=False)

                instance.mark1 = instance.mark1 - student_int.mark1
                instance.mark2 = instance.mark2 - student_int.mark2
                instance.mark3 = instance.mark3 - student_int.mark3
                instance.mark4 = instance.mark4 - student_int.mark4
                instance.mark5 = instance.mark5 - student_int.mark5
                instance.mark6 = instance.mark6 - student_int.mark6
                instance.markl1 = instance.markl1 - student_int.markl1
                instance.markl2 = instance.markl2 - student_int.markl2
                instance.markl3 = instance.markl3 - student_int.markl3
                instance.markl4 = instance.markl4 - student_int.markl4

                instance.branch = branch
                # print(instance.branch)

                instance.save()
                return render(request, 'student/home.html')

            else:
                # print("else")
                instance = marklist.save(commit=False)
                # print(instance.mark1)
                instance.branch = request.user.dept
                # print(instance.branch)

                instance.save()
                return render(request, 'student/home.html')

        context = {
            "form": marklist,
            "title": 'Add Marklist',

        }

        return render(request, 'student/marklist_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


def StudentUpdate(request, pk):
    instance = get_object_or_404(Student, regno=pk)
    student = Studentupdateform(request.POST or None, request.FILES or None, instance=instance)
    print("errr ", student.errors)
    logger.info("URL %s calls StudentUpdate() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    if student.is_valid():
        instance = student.save(commit=False)
        instance.save()

        return render(request, 'student/home.html')

    context = {
        "form": student,
        "title": 'Edit Student',
    }

    return render(request, 'student/student_form.html', context)


def MarklistUpdate(request, regno, branch, cursem, section, type):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='Faculty') or request.user.groups.filter(name='HOD'):

        instance = get_object_or_404(Marklist, regno=regno, cursem=cursem, branch=branch, section=section, type=type)
        student = MarklistForm(request.POST or None, instance=instance)
        logger.info("URL %s calls MarklistUpdate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if student.is_valid():
            if request.POST['type'] == 'External':
                chance = request.POST['chance']
                cursem = request.POST['cursem']
                branch = request.user.dept

                student_int = Marklist.objects.get(regno=regno, chance=chance, type='Internal', cursem=cursem,
                                                   branch=branch)

                instance = student.save(commit=False)
                instance.mark1 = instance.mark1 - student_int.mark1
                instance.mark2 = instance.mark2 - student_int.mark2
                instance.mark3 = instance.mark3 - student_int.mark3
                instance.mark4 = instance.mark4 - student_int.mark4
                instance.mark5 = instance.mark5 - student_int.mark5
                instance.mark6 = instance.mark6 - student_int.mark6
                instance.markl1 = instance.markl1 - student_int.markl1
                instance.markl2 = instance.markl2 - student_int.markl2
                instance.markl3 = instance.markl3 - student_int.markl3
                instance.markl4 = instance.markl4 - student_int.markl4

                # print("insta",instance.mark1)
                instance.branch = branch
                # # print(instance.branch)

                instance.save()
                return render(request, 'student/home.html')

            else:
                # print("else")
                instance = student.save(commit=False)
                # print(instance.mark1)
                instance.branch = request.user.dept
                # print(instance.branch)

                instance.save()
                return render(request, 'student/home.html')

        context = {
            "form": student,
            "title": 'Edit Marklist',

        }

        return render(request, 'student/marklist_form.html', context)


    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .models import Subject_Profile
from .forms import SubjectProfileAddForm


@login_required()
def Subject_ProfileCreate(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        subject_profile = SubjectProfileAddForm(request.POST or None)
        logger.info("URL %s calls Subject_ProfileCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if subject_profile.is_valid():
            instance = subject_profile.save(commit=False)
            instance.branch = request.user.dept
            instance.save()
            return render(request, 'student/home.html')

        context = {
            "form": subject_profile
        }

        return render(request, 'student/subject_profile_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


@login_required()
def SyllabusCreate(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        syllabus = Syllabusmodelform(request.POST or None)
        logger.info("URL %s calls SyllabusCreate() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        if syllabus.is_valid():
            instance = syllabus.save(commit=False)
            # print(instance.branch)
            instance.dept = request.user.dept
            # print(instance.branch)

            instance.save()
            return render(request, 'student/home.html')

        context = {
            "form": syllabus
        }

        return render(request, 'student/syllabus_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


class Subject_ProfileEdit(UpdateView):
    # logger.info("URL %s calls Subject_ProfileEdit() ",request.get_full_path())
    # logger.info("username %s ",request.user.username)
    model = Subject_Profile
    fields = '__all__'
    success_url = reverse_lazy('student:index')


# syllabus

from .models import Syllabus

from .filters import SyllabusFilter


@login_required()
def syllabus_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        syllabus_list = Syllabus.objects.all().order_by('dept')
        logger.info("URL %s calls syllabus_search() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        syllabus_filter = SyllabusFilter(request.GET, queryset=syllabus_list)

        return render(request, 'student/syllabus_list.html', {'filter': syllabus_filter})

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .forms import Syllabusmodelform, MarklistUpdateForm


# @login_required()
# def MarklistUpdate(request, pk):
#     instance = get_object_or_404(Marklist, regno=pk)
#     student = MarklistUpdateForm(request.POST or None, instance=instance)
#     if student.is_valid():
#         instance = student.save(commit=False)
#         instance.save()
#
#         return render(request, 'student/home.html')
#     context = {
#         "form": student,
#     }
#
#     return render(request, 'student/student_form.html', context)


def StudentUpdate(request, pk):
    instance = get_object_or_404(Student, regno=pk)
    logger.info("URL %s calls StudentUpdate() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    student = Studentupdateform(request.POST or None, request.FILES or None, instance=instance)
    if student.is_valid():
        instance = student.save(commit=False)
        instance.save()

        return render(request, 'student/home.html')
    context = {
        "form": student,
        "title": 'Edit Student',
    }

    return render(request, 'student/student_form.html', context)


# class SyllabusEdit(UpdateView):
#     model = Syllabus
#     #  form_class = SyllabusForm
#     fields = '__all__'
#     success_url = reverse_lazy('student:index')


from .forms import Syllabusupdateform


@login_required()
def SyllabusEdit(request, pk):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):
        instance = get_object_or_404(Syllabus, id=pk)
        logger.info("URL %s calls SyllabusEdit() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        syllabus = Syllabusupdateform(request.POST or None, instance=instance)
        if syllabus.is_valid():
            instance = syllabus.save(commit=False)
            instance.save()

            return render(request, 'student/home.html')
        context = {
            "form": syllabus,
            "title": 'Edit Syllabus',
        }

        return render(request, 'student/syllabus_form.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


def SyllabusDetail(request, regno):
    list = get_list_or_404(Syllabus, pk=regno)
    logger.info("URL %s calls SyllabusDetail() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    # marklist=get_list_or_404(Marklist,pk=regno)

    context = {'list': list,

               }
    return render(request, 'student/syllabus_detail.html', context)


from .models import Subject_Profile


# regno_id__regno__icontains
@login_required()
def subjectprofileview(request, id):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):
        # syllabus = Subject_Profile.objects.filter(syllabussubid=id)
        subjects = get_list_or_404(Subject_Profile, syllabussubid_id__id__icontains=id)
        syllabus_name = get_list_or_404(Syllabus, id__iexact=id)
        logger.info("URL %s calls subjectprofileview() ", request.get_full_path())
        logger.info("username %s ", request.user.username)

        context = {'list': subjects,
                   'syllabus': syllabus_name,
                   'title': 'Syllabus Profile',
                   }

        return render(request, 'student/syllabus_detail.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from .forms import SubjectProfileForm


def subjectprofileedit(request, id):
    subjectprofileformset = modelformset_factory(Subject_Profile, form=SubjectProfileForm, extra=0)
    queryset = Subject_Profile.objects.filter(syllabussubid_id__id__icontains=id).order_by('code')
    values = get_list_or_404(Subject_Profile, syllabussubid_id=id)
    syllabus_name = get_list_or_404(Syllabus, id=id)
    logger.info("URL %s calls subjectprofileedit() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    formset = subjectprofileformset(request.POST or None, queryset=queryset)
    # print("+++++++++++++++++++", values)
    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            # record=instance.cleaned_data()
            instance.save()

    context = {'form': formset,
               'branch': values[0].branch,
               'name': syllabus_name[0].year,
               'title': 'Edit Syllabus Subject',

               }

    return render(request, 'student/subjectprofile_form.html', context)


from .forms import RollnoRegnoMapAddForm


def RollnoRegnoMapAdd(request):
    form = RollnoRegnoMapAddForm(request.POST or None)
    logger.info("URL %s calls RollnoRegnoMapAdd() ", request.get_full_path())
    logger.info("username %s ", request.user.username)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return render(request, 'student/home.html')

    context = {"form": form, }

    return render(request, 'student/rollnoregnomap_form.html', context)


# def RollnoRegnoMapEdit(request):


from .models import RollnoRegnoMap

from .filters import AttendenceFilter

from .forms import SubjectProfileForm, RollnoRegnoMapEditForm


def attendenceedit(request, year, branch, cursem, section):
    logger.info("URL %s calls attendenceedit() ", request.get_full_path())
    logger.info("username %s ", request.user.username)
    subjectprofileformset = modelformset_factory(RollnoRegnoMap, form=RollnoRegnoMapEditForm, extra=0)
    queryset = RollnoRegnoMap.objects.filter(year=year, cursem=cursem, branch=branch, section=section)
    # regno_list = RollnoRegnoMap.objects.filter(id__icontains=id).order_by('rollno').values_list('regno')

    names = get_list_or_404(Student, join=year, cursem=cursem, branch=branch, section=section)
    reg_map = get_list_or_404(RollnoRegnoMap, year=year, cursem=cursem, branch=branch, section=section)

    subject = get_list_or_404(Subject_Profile, sem=cursem, branch=branch)

    # values = get_list_or_404(Subject_Profile, syllabussubid_id=id)
    # syllabus_name = get_list_or_404(Syllabus, id=id)
    # print(names)
    # print("no of students ", len(names))
    # print(reg_map)

    # print(subject)
    print("post data ", request.POST)
    formset = subjectprofileformset(request.POST or None, queryset=queryset)
    print("formset ", formset)
    print("+++++++++++++++++++err ", formset.errors)

    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            # record=instance.cleaned_data()
            print("scsccs ", instance)
            instance.save()
            print("saved")

    context = {'form': formset,
               'names': names[0].name,
               'semester': names[0].cursem,
               'branch': names[0].branch,
               'facultyname': reg_map[0].facultyid.ename,
               'facultydept': reg_map[0].facultyid.dept,
               # 'facultyid':reg_map[0].facultyid.id,
               'subjectname': subject[0].name,
               'subjectcode': subject[0].code,
               'id': reg_map[0].id

               }

    return render(request, 'student/rollnoregno_edit_form.html', context)


@login_required()
def syllabus_search(request):
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(name='Admin'):

        syllabus_list = Syllabus.objects.filter(dept=request.user.dept).order_by('dept')
        syllabus_filter = SyllabusFilter(request.GET, queryset=syllabus_list)
        logger.info("URL %s calls syllabus_search() ", request.get_full_path())
        logger.info("username %s ", request.user.username)
        context = {
            'filter': syllabus_filter,
            'title': 'Syllabus Search',
        }

        return render(request, 'student/syllabus_list.html', context)

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


from csv import DictWriter
from io import StringIO
from .resources import AttendenceResource


def attendence_list_pdf(request):
    if request.method == 'GET':
        branch = request.GET['branch']
        cursem = request.GET['cursem']
        section = request.GET['section']
        facultyid = request.GET['facultyid']
        subcode = request.GET['subcode']
        logger.info("URL %s calls attendence_list_pdf() ", request.get_full_path())
        logger.info("username %s ", request.user.username)

        total = []
        present_total = []
        absent_total = []
        ptotal = 0
        atotal = 0
        prev_atotal = 0
        prev_ptotal = 0
        prev_name = ""

        list = RollnoRegnoMap.objects.filter(branch=branch, cursem=cursem, section=section).order_by('regno', )

        for student in list:
            if student.atotal == -1:
                atotal = 0

            if student.ptotal == -1:
                ptotal = 0

            if prev_name == student.name:
                atotal = prev_atotal
                ptotal = prev_ptotal
            else:
                atotal = 0
                ptotal = 0

            if student.firsthr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.secondhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.thirdhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.fourthhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.fifthhr == "P":
                ptotal = ptotal + 1
                # present_total.append(ptotal)

            if student.sixthhr == "P":
                ptotal = ptotal + 1

            present_total.append(ptotal)

            if student.firsthr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.secondhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.thirdhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.fourthhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.fifthhr == "A":
                atotal = atotal + 1
                # present_total.append(atotal)

            if student.sixthhr == "A":
                atotal = atotal + 1

            prev_name = student.name
            prev_ptotal = ptotal
            prev_atotal = atotal
            absent_total.append(atotal)
            total.append(atotal + ptotal)
            # print("id ",student.id) 
            RollnoRegnoMap.objects.filter(id=student.id, branch=branch, cursem=cursem, section=section).update(
                atotal=atotal, ptotal=ptotal, )

        list = RollnoRegnoMap.objects.filter(branch=branch, cursem=cursem, section=section,
                                             facultyid=facultyid, subjectcode=subcode).order_by('cursem', 'rollno',
                                                                                                'time')

        context = {'list': list,
                   'facultyid': facultyid,
                   'subcode': subcode,
                   'cursem': cursem,
                   'branch': branch,
                   'section': section,
                   }


        attendence_resource = AttendenceResource()
        dataset = attendence_resource.export(queryset=list)
        return HttpResponse(dataset.csv, content_type='text/csv')

        # f = StringIO()
        # writer = DictWriter(f, ["Tipo de Factura", "Descripcion", "Precio", "Subtotal", "total", "paid"])
        # writer.writeheader()
        # report_line = {
        #     "Tipo de Factura": fact.tipo_Factura,
        #     "Descripcion": fact.descripcion,
        #     ...
        # }
        # writer.writerow(report_line)
        # report = f.getvalue()
        # resp = HttpResponse(report, mimetype="application/octet-stream")
        # resp["Content-Disposition"] = "attachment  filename='{}'".format("report.csv")
        # return resp

        # html_string = render_to_string('student/attendence_pdf_view.html', context)
        # html = HTML(string=html_string)
        # doc = html.render()
        # pdf = doc.write_pdf()
        # # pdf['Content-Disposition']='inline filename:attendem.pdf'
        # # pdf['Content-Disposition'] = 'attachment filename:attendence.pdf'
        # return HttpResponse(pdf, content_type='application/pdf')

        # return render(request, 'student/attendence_pdf_view.html', context)


def attendence_pdf(request):
    logger.info("URL %s calls attendence_pdf()", request.get_full_path())
    logger.info("username %s ", request.user.username)
    return render(request, 'student/attendence_pdf_search.html')


@login_required()
def attendence_search(request):
    # print("ddd ",request.user.first_name)
    faculty = None
    if request.user.groups.filter(name='Dataop') or request.user.groups.filter(
            name='Admin') or request.user.groups.filter(name='Faculty'):

        if request.method == "GET":

            attendence_list = RollnoRegnoMap.objects.all().order_by('cursem', 'rollno', 'time')
            logger.info("URL %s calls attendence_search() ", request.get_full_path())
            logger.info("username %s ", request.user.username)
            attendence_filter = AttendenceFilter(request.GET, queryset=attendence_list)

            # print("req data111 ", request.GET['subcode'])

            # facultyid = request.GET['facultyid']
            # print("********** ",request.GET['facultyid'])
            # subcode = request.GET['subjectcode']

            if request.user.groups.filter(name='Faculty'):
                faculty = Faculty.objects.filter(ename=request.user.first_name)
            # print("ss ",faculty[0].empid) 

            return render(request, 'student/rollnoregnomap_list.html', {'filter': attendence_filter,
                                                                        'title': 'Search Attendence',
                                                                        'faculty': faculty,
                                                                        # 'fac_id': facultyid,
                                                                        # 'subcode': subcode,
                                                                        #
                                                                        })

    else:
        context = {"perm_error": 'You do not have permission to access this page'}

        return render(request, 'student/login.html', context)


# from .models import RollnoRegnoMap

#
# class RollnoRegnoMapAdd(CreateView):
#     model = RollnoRegnoMap
#     fields = '__all__'
#     success_url = reverse_lazy('student:index')
#
#
# class RollnoRegnoMapEdit(UpdateView):
#     model = RollnoRegnoMap
#     fields = '__all__'
#     success_url = reverse_lazy('student:index')

# #
# from .models import StudentFacultyLabMap
#
#
# #
# class StudentFacultyLabMapAdd(CreateView):
#     model = StudentFacultyLabMap
#     fields = '__all__'
#     success_url = reverse_lazy('student:index')
#
#
#
# class StudentFacultyLabMapEdit(UpdateView):
#     model = StudentFacultyLabMap
#     fields = '__all__'
#     success_url = reverse_lazy('student:index')
#
#
# from .forms import StudentFacultyLabMapAddForm
#
#
# def StudentFacultyLabMapAdd(request):
#     labmap = StudentFacultyLabMapAddForm(request.POST or None)
#
#     if labmap.is_valid():
#         instance = labmap.save(commit=False)
#
#         instance.save()
#         return render(request, 'student/home.html')
#
#     context = {
#         "form": labmap,
#     }
#
#     return render(request, 'student/studentfacultylabmap_form.html',context)
#

@login_required()
def facultyattendancepage(request):
    obj = ClassAttendanceMap.objects.get_or_create(pk=1,)
    lst = []
    for i in range(1, 101):

        lst.append(getattr(obj, 'r' + str(i)))
    return render(request, 'student/faculty_attendance_main.html', {'model': obj})
