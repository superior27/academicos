# -*- encoding: utf-8 -*-
from academicos.core.models import Student, Teacher, Class, Grade, Matriculation
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
	fields = ('name','matriculation_number','date_birth','gender','street','street_number','street_complement','neighborhood','city','state','postal_code',
            'phone','allergy','health_plan','emergency_name','emergency_phone','father_name','father_phone','father_rg',
            'father_cpf','father_profession','father_instruction','father_date_birth','mother_name','mother_phone','mother_rg',
            'mother_cpf','mother_profession','mother_instruction','mother_date_birth','responsible_financial_name',
            'responsible_financial_phone','responsible_financial_rg','responsible_financial_cpf','responsible_financial_date_birth',
            'responsible_financial_email','observation','user')
	list_display = ('name','matriculation_number','responsible_financial_name','date_birth')

class TeacherAdmin(admin.ModelAdmin):
	fields = ('name','date_birth','rg','cpf','phone','email','user')
	list_display = ('name','cpf')

class ClassAdmin(admin.ModelAdmin):
	fields = ('name','teacher')
	list_display = ('name','teacher')

class GradeAdmin(admin.ModelAdmin):
	fields = ('name', 'room','shift','classes')
	list_display = ('name','room','shift')

class MatriculationAdmin(admin.ModelAdmin):
	fields = ('students','grade')
	list_display = ('grade',)

admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Matriculation,MatriculationAdmin)