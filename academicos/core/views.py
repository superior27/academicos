# -*- encoding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forms import RegisterForm, StudentRegisterForm, TeacherRegisterForm, ClassRegisterForm, GradeRegisterForm
from forms import MatriculationRegisterForm, DisciplinaRegisterForm, DisciplinaAlterarForm, FinanceiroAlterarForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from models import MyUser, Disciplina, Student, Teacher
from datetime import datetime
import datetime
import pyboleto
from pyboleto.bank.real import BoletoReal
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.bank.caixa import BoletoCaixa
from pyboleto.bank.bancodobrasil import BoletoBB
from pyboleto.bank.santander import BoletoSantander
from pyboleto.pdf import BoletoPDF
from reportlab.pdfgen import canvas
from StringIO import StringIO
from datetime import date




@login_required
def homepage(request):
    return render(request, 'bemvindo.html')

@permission_required('core.administration')
@login_required
def register(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

@permission_required('core.administration')
@login_required
def new(request):
    return render(request,'register_form.html',
        {'form' : RegisterForm()})

@permission_required('core.administration')
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
    if codename == 'administration':
        permission = Permission.objects.get(content_type=content_type, codename='desk')
        obj.user_permissions.add(permission)

    return HttpResponseRedirect('/register/%d/' % obj.pk)

@login_required
def detail(request, pk):
    register = get_object_or_404(User, pk=pk)
    return render(request, 'register_detail.html',
        {'register' : register})

@permission_required('core.desk')
@login_required
def student_register(request):
    if request.method == 'POST':
        return student_create(request)
    else:
        return student_new(request)

@permission_required('core.desk')
@login_required
def student_new(request):
    return render(request,'student_register_form.html',
        {'form' : StudentRegisterForm()})

@permission_required('core.desk')
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
    today = datetime.datetime.now()
    obj.matriculation_number = str(today.year)+str(user.id)
    obj.user = user
    obj.save()
    return render(request,'register_detail.html',{})

@permission_required('core.desk')
@login_required
def teacher_register(request):
    if request.method == 'POST':
        return teacher_create(request)
    else:
        return teacher_new(request)

@permission_required('core.desk')
@login_required
def teacher_new(request):
    return render(request,'teacher_register_form.html',
        {'form' : TeacherRegisterForm()})

@permission_required('core.desk')
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

@permission_required('core.desk')
@login_required
def class_register(request):
    if request.method == 'POST':
        return class_create(request)
    else:
        return class_new(request)

@permission_required('core.desk')
@login_required
def class_new(request):
    return render(request,'class_register_form.html',
        {'form' : ClassRegisterForm()})

@permission_required('core.desk')
@login_required
def class_create(request):
    form = ClassRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'class_register_form.html',
            {'form' : ClassRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@permission_required('core.desk')
@login_required
def grade_register(request):
    if request.method == 'POST':
        return grade_create(request)
    else:
        return grade_new(request)

@permission_required('core.desk')
@login_required
def grade_new(request):
    return render(request,'grade_register_form.html',
        {'form' : GradeRegisterForm()})

@permission_required('core.desk')
@login_required
def grade_create(request):
    form = GradeRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'grade_register_form.html',
            {'form' : GradeRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@permission_required('core.desk')
@login_required
def matriculation_register(request):
    if request.method == 'POST':
        return matriculation_create(request)
    else:
        return matriculation_new(request)

@permission_required('core.desk')
@login_required
def matriculation_new(request):
    return render(request,'matriculation_register_form.html',
        {'form' : MatriculationRegisterForm()})

@permission_required('core.desk')
@login_required
def matriculation_create(request):
    form = MatriculationRegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'matriculation_register_form',
            {'form' : MatriculationRegisterForm()})
    obj = form.save()
    return HttpResponseRedirect('/register/%d/' % obj.pk)

@permission_required('core.desk')
@login_required
def disciplina_register(request):
    if request.method == 'POST':
        return disciplina_create(request)
    else:
        return disciplina_new(request)

@permission_required('core.desk')
@login_required
def disciplina_new(request):
    return render(request,'disciplina_register_form.html',
        {'form' : DisciplinaRegisterForm()})

@permission_required('core.desk')
@login_required
def disciplina_create(request):
    user_aluno = ''
    form = DisciplinaRegisterForm(request.POST)
    if not form.is_valid():
        return render(request,'disciplina_register_form.html',
            {'form' : DisciplinaRegisterForm()})
    Aluno = form.cleaned_data['aluno']
    for alunoOb in Aluno:
        meu_aluno2 = Student.objects.get(id=alunoOb.id)
        Professor = form.cleaned_data['professor']
        meu_professor2 = Teacher.objects.get(id=Professor.id)        
        obj = Disciplina()
        obj.nome = form.cleaned_data['nome']
        obj.professor = form.cleaned_data['professor']
        obj.aluno = meu_aluno2
        obj.serie = form.cleaned_data['serie']
        obj.turma = form.cleaned_data['turma']
        obj.turno = form.cleaned_data['turno']
        obj.ano = form.cleaned_data['ano']
        obj.save()
        nomeGrupo = obj.get_serie_display() + " Turma: " + obj.get_turma_display() + " Turno: " + obj.get_turno_display()
        GrupoQuery = Group.objects.filter(name = nomeGrupo)
        if not GrupoQuery:
            NovoGrupo = Group.objects.create(name=nomeGrupo)
        else:
            NovoGrupo = Group.objects.get(name=nomeGrupo)
        aluno = obj.aluno
        user_aluno = User.objects.get(username=aluno.name)
        user_aluno.groups.add(NovoGrupo)

    return render(request,'register_detail.html',{'grupos' : Group.objects.filter(user=user_aluno)})

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


@login_required
@permission_required('core.desk', login_url='/')
def menu_secretaria(request):
    return render(request,'menu_secretaria.html',{})

@login_required
@permission_required('core.desk', login_url='/')
def lista_alunos_matricula(request):
    lista_aluno = Student.objects.all()
    return render(request,'lista_alunos_matricula.html', {'lista_aluno' : lista_aluno})

@login_required
@permission_required('core.desk',login_url='/')
def matricula_detail(request, pk):
    form = get_object_or_404(Student,pk=pk)
    aux = Group.objects.filter(user=form.user)
    i = aux.count() - 1
    return render(request,'matricula_detail.html',{'form':form,'resto':aux[i],'data':datetime.datetime.now()})

@login_required
@permission_required('core.desk',login_url='/')
def lista_alunos_historico(request):
    lista_aluno = Student.objects.all()
    return render(request,'lista_alunos_historico.html',{'lista_aluno':lista_aluno})

@login_required
@permission_required('core.desk',login_url='/')
def historico_detail(request,pk):
    form = get_object_or_404(Student,pk=pk)
    lista_disciplina = Disciplina.objects.filter(aluno=form).order_by('ano')
    return render(request,'historico_detail.html',{'form':form, 'lista_disciplina':lista_disciplina})

@login_required
@permission_required('core.desk',login_url='/')
def lista_alunos_financeiro(request):
    lista_aluno = Student.objects.all()
    return render(request,'lista_alunos_financeiro.html',{'lista_aluno':lista_aluno})



@login_required
@permission_required('core.desk',login_url='/')
def financeiro_alterar(request, pk):
    aluno = get_object_or_404(Student,pk=pk)
    if request.method == "POST":
        form = FinanceiroAlterarForm(request.POST,instance=aluno)
        if form.is_valid():
            obj = form.save()            
            return render(request, 'register_detail.html',{})
    else:
        form = FinanceiroAlterarForm(instance=aluno)
            
    return render(request, 'financeiro_alterar.html',
        {'form' : form,'aluno' : aluno})

@login_required
@permission_required('core.desk',login_url='/')
def lista_aluno_alterar(request):
    lista_aluno = Student.objects.all()
    return render(request,'lista_alunos_alterar.html',{'lista_aluno':lista_aluno})

@login_required
@permission_required('core.desk',login_url='/')
def aluno_alterar(request, pk):
    aluno = get_object_or_404(Student,pk=pk)
    if request.method == "POST":
        form = StudentRegisterForm(request.POST,instance=aluno)
        if form.is_valid():
            obj = form.save()            
            return render(request, 'register_detail.html',{})
    else:
        form = StudentRegisterForm(instance=aluno)
            
    return render(request, 'financeiro_alterar.html',
        {'form' : form,'aluno' : aluno})

@login_required
@permission_required('core.desk',login_url='/')
def lista_professor_alterar(request):
    lista_professor = Teacher.objects.all()
    return render(request,'lista_professor_alterar.html',{'lista_professor':lista_professor})


@login_required
@permission_required('core.desk',login_url='/')
def professor_alterar(request, pk):
    """
    Está com as mesmas variáveis para reaproveitar o template
    """
    aluno = get_object_or_404(Teacher,pk=pk)
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST,instance=aluno)
        if form.is_valid():
            obj = form.save()            
            return render(request, 'register_detail.html',{})
    else:
        form = TeacherRegisterForm(instance=aluno)
            
    return render(request, 'financeiro_alterar.html',
        {'form' : form,'aluno' : aluno})


@login_required
@permission_required('core.desk',login_url='/')
def lista_disciplina_adm(request):
    lista_disciplina = Disciplina.objects.all()
    return render(request,'lista_disciplina_professor.html',
        {'lista_disciplina' : lista_disciplina})



@login_required
@permission_required('core.desk',login_url='/')
def lista_aluno_boleto(request):
    lista_aluno = Student.objects.all()
    return render(request,'lista_alunos_boleto.html',{'lista_aluno':lista_aluno})





@permission_required('core.desk')
def print_santander(request):
    listaDadosSantander = []
    for i in range(12):
        d = BoletoSantander()
        d.agencia_cedente = '1333'
        d.conta_cedente = '0707077'
        d.data_vencimento = datetime.date(2013, (i+1), 22)
        d.data_documento = datetime.date(2013, 7, 17)
        d.data_processamento = datetime.date(2012, 7, 17)
        d.valor_documento = 2952.95
        d.nosso_numero = '1234569'
        d.numero_documento = '12347'
        d.ios = '0'

        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = "Rua Acme, 123 - Centro - Sao Paulo/SP - CEP: 12345-678"

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = 255.00

        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDadosSantander.append(d)

    # Caixa Formato normal - uma pagina por folha A4
    buffer = StringIO()
    boleto = BoletoPDF(buffer)
    #boleto = canvas.Canvas(response)
    for i in range(len(listaDadosSantander)):
        boleto.drawBoleto(listaDadosSantander[i])
        boleto.nextPage()
    #boleto.showPage()
    boleto.save()

    pdf_file = buffer.getvalue()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % (
        u'boletos_%s.pdf' % (
            date.today().strftime('%Y%m%d'),
        ),
    )
    response.write(pdf_file)

    return response



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
