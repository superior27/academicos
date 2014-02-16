# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from models import Student, Teacher, Class, Grade, Matriculation, Disciplina, MyUser
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType




class RegisterForm(UserCreationForm):
    PERMISSIONS_CHOICE = (
        ('S', 'Estudante'),
        ('T', 'Professor'),
        ('D', u'Secretária'),
        ('A', u'Administração'),
        )
    username = forms.CharField(label="Loguin")
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label="Sobrenome")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    permissions = forms.ChoiceField(PERMISSIONS_CHOICE)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2','permissions')

class PhoneWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets =(
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs))
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if not value:
            return [None, None]
        return value.split('-')

class PhoneField(forms.MultiValueField):
    widget = PhoneWidget

    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
            forms.IntegerField())
        super(PhoneField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list:
            return ''
        if data_list[0] in EMPTY_VALUES:
            raise forms.ValidationError(_(u'DDD inválido.'))
        if data_list[1] in EMPTY_VALUES:
            raise forms.ValidationError(_(u'Número inválido'))
        return '%s-%s' % tuple(data_list)




class StudentRegisterForm(forms.ModelForm):
    
    
    class Meta:
        model = Student
        fields = ('name','date_birth','gender','street','street_number','street_complement','neighborhood','city','state','postal_code',
            'phone','allergy','health_plan','emergency_name','emergency_phone','father_name','father_phone','father_rg',
            'father_cpf','father_profession','father_instruction','father_date_birth','mother_name','mother_phone','mother_rg',
            'mother_cpf','mother_profession','mother_instruction','mother_date_birth','responsible_financial_name',
            'responsible_financial_phone','responsible_financial_rg','responsible_financial_cpf','responsible_financial_date_birth',
            'responsible_financial_email','observation')

class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name','date_birth','rg','cpf','phone','email')

class ClassRegisterForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('name','teacher')

class GradeRegisterForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = 'name','room','shift','classes'

class MatriculationRegisterForm(forms.ModelForm):
    class Meta:
        model = Matriculation
        fields = 'students','grade'

class DisciplinaRegisterForm(forms.ModelForm):
    content_type = ContentType.objects.get_for_model(MyUser)
    permission = Permission.objects.get(content_type=content_type, codename='student')
    aluno = forms.ModelMultipleChoiceField(queryset = Student.objects.all())
    class Meta:
        model = Disciplina
        fields = 'nome','professor','serie','turma','turno','ano'

class DisciplinaAlterarForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = 'nota1','nota2','nota3','nota4','recuperacao1','carga_horaria'

class FinanceiroAlterarForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = 'name','financial'
        



"""class turmasForm(forms.ModelForm):
    class Meta:
        model = turmas
        fields = 'grade'"""