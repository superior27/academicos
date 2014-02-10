# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime


class Teacher(models.Model):
    name = models.CharField(_(u'Nome'),max_length=100)
    date_birth = models.DateField(_(u'Data de Nascimento'))
    rg = models.CharField(max_length=11)
    cpf = models.CharField(max_length=11)
    phone = models.CharField(_(u"Telefone"),max_length=13)
    email = models.EmailField(_(u"E-mail"))
    user = models.ForeignKey(User,blank=True,null=True)
    
    u"""Como o meu objeto será visto"""
    def __unicode__(self):
        return u'%s' % (self.name)




class Student(models.Model):
    
    GENDER_CHOICE = (
        ('M','Masculino'),
        ('F','Feminino'),)

    name = models.CharField(_(u'Nome'), max_length=100)
    matriculation_number = models.CharField(_(u'Número de Matrícula'),max_length=100,blank=True,null=True)
    date_birth = models.DateField(_(u'Data de Nascimento'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_complement = models.CharField(max_length=100,blank=True,null=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=8)
    phone = models.CharField(max_length=13)
    allergy = models.TextField(max_length=100,blank=True,null=True)
    health_plan = models.CharField(max_length=100,blank=True,null=True)
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=13)
    father_name = models.CharField(max_length=100,blank=True,null=True)
    father_phone = models.CharField(max_length=13,blank=True,null=True)
    father_rg = models.CharField(max_length=11,blank=True,null=True)
    father_cpf = models.CharField(max_length=11,blank=True,null=True)
    father_profession = models.CharField(max_length=100,blank=True,null=True)
    father_instruction = models.CharField(max_length=100,blank=True,null=True)
    father_date_birth = models.DateField(_('data de nascimento do pai'),blank=True,null=True)
    mother_name = models.CharField(max_length=100,blank=True,null=True)
    mother_phone = models.CharField(max_length=13,blank=True,null=True)
    mother_rg = models.CharField(max_length=11,blank=True,null=True)
    mother_cpf = models.CharField(max_length=11,blank=True,null=True)
    mother_profession = models.CharField(max_length=100,blank=True,null=True)
    mother_instruction = models.CharField(max_length=100,blank=True,null=True)
    mother_date_birth = models.DateField(_('data de nascimento da mae'),blank=True,null=True)
    responsible_financial_name = models.CharField(_(u'Nome do Responsável Financeiro'), max_length=100)
    responsible_financial_phone = models.CharField(max_length=13)
    responsible_financial_rg = models.CharField(max_length=11)
    responsible_financial_cpf = models.CharField(max_length=11)
    responsible_financial_date_birth = models.DateField(_('data de nascimento do responsavel financeiro'))
    responsible_financial_email = models.EmailField(blank=True,null=True)
    user = models.ForeignKey(User,blank=True,null=True)
    observation = models.TextField(max_length=100,blank=True,null=True)    
    def __unicode__(self):
        return u'%s - %s' % (self.name,self.matriculation_number)


class Disciplina(models.Model):
    TURNO_CHOICES = (
        ('M',u'Manhã'),
        ('V',u'Tarde'),
        ('N',u'Noite'),

        )
    SERIE_CHOICES = (
        (u'M1',u'Maternal 1'),
        (u'M2',u'Maternal 2'),
        (u'J1',u'Jardim 1'),
        (u'J2',u'Jardim 2'),
        (u'F1',u'1º Ano Fundamental'),
        (u'F2',u'2º Ano Fundamental'),
        (u'F3',u'3º Ano Fundamental'),
        (u'F4',u'4º Ano Fundamental'),
        (u'F5',u'5º Ano Fundamental'),
        (u'F6',u'6º Ano Fundamental'),
        (u'F7',u'7º Ano Fundamental'),
        (u'F8',u'8º Ano Fundamental'),
        (u'F9',u'9º Ano Fundamental'),
        (u'M1',u'1º Ano Ensino Médio'),
        (u'M2',u'2º Ano Ensino Médio'),
        (u'M3',u'3º Ano Ensino Médio'),
        (u'O',u'Outra'),
        )
    TURMA_CHOICES = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),

        ) 
    nome = models.CharField(_(u'Nome'),max_length=100)
    nota1 = models.DecimalField(_(u'Nota 1'),max_digits=10,decimal_places=3,blank=True,null=True)
    nota2 = models.DecimalField(_(u'Nota 2'),max_digits=10,decimal_places=3,blank=True,null=True)
    nota3 = models.DecimalField(_(u'Nota 3'),max_digits=10,decimal_places=3,blank=True,null=True)
    nota4 = models.DecimalField(_(u'Nota 4'),max_digits=10,decimal_places=3,blank=True,null=True)
    recuperacao1 = models.DecimalField(_(u'Recuperação'),max_digits=10,decimal_places=3,blank=True,null=True)
    recuperacao2 = models.DecimalField(_(u'Recuperação 2'),max_digits=10,decimal_places=3,blank=True,null=True)
    media = models.DecimalField(_(u'Média'),max_digits=10,decimal_places=3,blank=True,null=True)
    carga_horaria = models.DecimalField(_(u'Carga Horária'),max_digits=10,decimal_places=3,blank=True,null=True)
    professor = models.ForeignKey(Teacher)
    turno = models.CharField(_(u'Turno'),max_length=2,choices=TURNO_CHOICES)
    serie = models.CharField(_(u'Série'),max_length=3,choices=SERIE_CHOICES)
    turma = models.CharField(_(u'Turma'),max_length=1,choices=TURMA_CHOICES)
    ano = models.CharField(_(u'Ano'),max_length=4)
    aluno = models.ForeignKey(Student,blank=True,null=True)
    def __unicode__(self):
        return u'%s - %s - %s -%s - %s' % (self.nome,self.serie,self.turma,self.turno,self.ano)





class Class(models.Model):
    name = models.CharField(_(u'Nome'),max_length=100)
    teacher = models.ForeignKey(Teacher)
    def __unicode__(self):
        return u'%s' % (self.name)

class Grade(models.Model):
    name = models.CharField(_(u'Nome'),max_length=100)
    room = models.CharField(_(u'Turma'),max_length=100)
    shift = models.CharField(_(u'Turno'),max_length=100)
    classes = models.ManyToManyField(Class)
    def __unicode__(self):
        return u'%s %s %s' % (self.name,self.room,self.shift)

class Matriculation(models.Model):
    students = models.ManyToManyField(Student)
    grade = models.ForeignKey(Grade)


class MyUser(models.Model):
    class Meta:
        permissions = (
            ('student','Is Student'),
            ('teacher','Is Teacher'),
            ('desk','Is Desk'),
            ('administration','Is Administration'),
            )

"""class turmas(models.Model):
    
    Aqui é a Grade
    
    grade = models.ForeignKey(Grade)"""



