# -*- encoding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forms import RegisterForm, StudentRegisterForm, TeacherRegisterForm, ClassRegisterForm, GradeRegisterForm
from forms import MatriculationRegisterForm, DisciplinaRegisterForm, DisciplinaAlterarForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from models import MyUser, Disciplina, Student, Teacher
from datetime import datetime

@login_required
def homepage(request):
    return render(request, 'bemvindo.html')

@permission_required('core.student')
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
    obj = form.save(commit=False)
    user = User.objects.create_user(obj.name,'email@email.com',obj.responsible_financial_cpf)    
    content_type = ContentType.objects.get_for_model(MyUser)
    permission = Permission.objects.get(content_type=content_type, codename='student')
    user.user_permissions.add(permission)
    user.save()
    today = datetime.now()
    obj.matriculation_number = str(today.year)+str(user.id)
    obj.user = user
    obj.save()
    return render(request,'register_detail.html',{})

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
    obj = form.save(commit=False)
    user = User.objects.create_user(obj.name,obj.email,obj.cpf)    
    content_type = ContentType.objects.get_for_model(MyUser)
    permission = Permission.objects.get(content_type=content_type, codename='teacher')
    user.user_permissions.add(permission)
    user.save()
    obj.user = user
    obj.save()
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

@login_required
def disciplina_register(request):
    if request.method == 'POST':
        return disciplina_create(request)
    else:
        return disciplina_new(request)

@login_required
def disciplina_new(request):
    return render(request,'disciplina_register_form.html',
        {'form' : DisciplinaRegisterForm()})

@login_required
def disciplina_create(request):
    form = DisciplinaRegisterForm(request.POST)
    if not form.is_valid():
        return render(request,'disciplina_register_form.html',
            {'form' : DisciplinaRegisterForm()})
    obj = form.save()
    nomeGrupo = obj.get_serie_display() + " Turma: " + obj.get_turma_display() + " Turno: " + obj.get_turno_display()
    GrupoQuery = Group.objects.filter(name = nomeGrupo)
    if not GrupoQuery:
        NovoGrupo = Group.objects.create(name=nomeGrupo)
    else:
        NovoGrupo = Group.objects.get(name=nomeGrupo)
    aluno = obj.aluno
    user_aluno = User.objects.get(username=aluno.name)
    user_aluno.groups.add(NovoGrupo)

    return render(request,'register_detail.html',{'user',request.user})

@login_required
@permission_required('core.student',login_url='/')
def lista_disciplina_aluno(request):
    meu_aluno = Student.objects.get(user=request.user)
    lista_disciplina = Disciplina.objects.filter(aluno=meu_aluno)
    return render(request,'lista_disciplina_aluno.html',
        {'lista_disciplina' : lista_disciplina})

@login_required
@permission_required('core.student',login_url='/')
def disciplina(request, pk):
    form = get_object_or_404(Disciplina,pk=pk)
    return render(request,'disciplina.html',{'form':form})

@login_required
@permission_required('core.teacher',login_url='/')
def disciplina_alterar(request, pk):
    disciplina = get_object_or_404(Disciplina,pk=pk)
    if request.method == "POST":
        form = DisciplinaAlterarForm(request.POST,instance=disciplina)
        if form.is_valid():
            obj = form.save()
            if obj.nota1 and obj.nota2 and obj.nota3 and obj.nota4:
                obj.media = (obj.nota1+obj.nota2+obj.nota3+obj.nota4)/4
            if obj.recuperacao1:
                obj.media = (obj.media+obj.recuperacao1)/2
            obj.save()
            return render(request, 'register_detail.html',{})
    else:
        form = DisciplinaAlterarForm(instance=disciplina)
            
    return render(request, 'disciplina_professor.html',
        {'form' : form,'disciplina' : disciplina})

@login_required
@permission_required('core.student',login_url='/')
def menu_aluno(request):
    return render(request,'menu_aluno.html',{})

@login_required
@permission_required('core.teacher',login_url='/')
def menu_professor(request):
    return render(request,'menu_professor.html',{})

@login_required
@permission_required('core.teacher',login_url='/')
def lista_disciplina_professor(request):
    meu_professor = Teacher.objects.get(user=request.user)
    lista_disciplina = Disciplina.objects.filter(professor=meu_professor)
    return render(request,'lista_disciplina_professor.html',
        {'lista_disciplina' : lista_disciplina})

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
