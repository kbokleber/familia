from django.contrib import admin
from .models import FamilyMember, MedicalAppointment, MedicalProcedure

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'gender', 'relationship', 'blood_type')
    list_filter = ('gender', 'relationship')
    search_fields = ('name', 'relationship', 'emergency_contact')
    ordering = ('name',)

@admin.register(MedicalAppointment)
class MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ('family_member', 'doctor_name', 'specialty', 'appointment_date', 'location')
    list_filter = ('specialty', 'appointment_date')
    search_fields = ('family_member__name', 'doctor_name', 'specialty')
    ordering = ('-appointment_date',)

@admin.register(MedicalProcedure)
class MedicalProcedureAdmin(admin.ModelAdmin):
    list_display = ('family_member', 'procedure_name', 'procedure_date', 'doctor_name', 'location')
    list_filter = ('procedure_date',)
    search_fields = ('family_member__name', 'procedure_name', 'doctor_name')
    ordering = ('-procedure_date',)
