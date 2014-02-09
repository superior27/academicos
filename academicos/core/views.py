# -*- encoding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forms import RegisterForm, StudentRegisterForm, TeacherRegisterForm, ClassRegisterForm, GradeRegisterForm
from forms import MatriculationRegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from models import MyUser

@login_required
def homepage(request):
    return render(request, 'bemvindo.html')

@login_required
def register(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

@login_required
def new(request):
    return render(request,'register_form.html',
        {'form' : RegisterForm()})

@login_required
def create(request):
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'register_form.html',
            {'form' : RegisterForm()})

    obj = form.save()
    content_type = ContentType.objects.get_for_model(MyUser)
    type_user = form.cleaned_data['permissions']
    codename = ''
    
    if type_user == 'S':
        codename = 'student'
    
    elif type_user == 'T':
        codename='teacher'

    elif type_user == 'D':
        codename='desk'

    else :
        codename='administration'

    permission = permission = Permission.objects.get(content_type=content_type, codename=codename)
    obj.user_permissions.add(permission)
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def detail(request, pk):
    register = get_object_or_404(User, pk=pk)
    return render(request, 'register_detail.html',
        {'register' : register})

@login_required
def student_register(request):
    if request.method == 'POST':
        return student_create(request)
    else:
        return student_new(request)

@login_required
def student_new(request):
    return render(request,'student_register_form.html',
        {'form' : StudentRegisterForm()})

@login_required
def student_create(request):
    form = StudentRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'student_register_form.html',
            {'form' : StudentRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def teacher_register(request):
    if request.method == 'POST':
        return teacher_create(request)
    else:
        return teacher_new(request)

@login_required
def teacher_new(request):
    return render(request,'teacher_register_form.html',
        {'form' : TeacherRegisterForm()})

@login_required
def teacher_create(request):
    form = TeacherRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'teacher_register_form.html',
            {'form' : TeacherRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def class_register(request):
    if request.method == 'POST':
        return class_create(request)
    else:
        return class_new(request)

@login_required
def class_new(request):
    return render(request,'class_register_form.html',
        {'form' : ClassRegisterForm()})

@login_required
def class_create(request):
    form = ClassRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'class_register_form.html',
            {'form' : ClassRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def grade_register(request):
    if request.method == 'POST':
        return grade_create(request)
    else:
        return grade_new(request)

@login_required
def grade_new(request):
    return render(request,'grade_register_form.html',
        {'form' : GradeRegisterForm()})

@login_required
def grade_create(request):
    form = GradeRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'grade_register_form.html',
            {'form' : GradeRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def matriculation_register(request):
    if request.method == 'POST':
        return matriculation_create(request)
    else:
        return matriculation_new(request)

@login_required
def matriculation_new(request):
    return render(request,'matriculation_register_form.html',
        {'form' : MatriculationRegisterForm()})

@login_required
def matriculation_create(request):
    form = MatriculationRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'matriculation_register_form',
            {'form' : MatriculationRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

"""def turmas_register(request):
    if request.method == 'POST':
        return turmas_create(request)
    else:
        return turmas_new(request)

def turmas_new(request):
    return render(request,'turmas.html',
        {'form' : turmasForm()})

def turmas_create(request):
    form = turmasForm(request.POST)
    if not form.is_valid():
        return render(request, 'turmas.html',
            {'form' : turmasForm()})
    obj = form.save()

    return render('disciplinas':Grade.objects.filter(classes=obj.classes))


"""
