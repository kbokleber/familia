from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication
from .forms import FamilyMemberForm, MedicalAppointmentForm, MedicalProcedureForm, MedicationForm
from django.utils import timezone
from django.db.models import Q

@login_required
def healthcare_dashboard(request):
    """Dashboard principal do sistema de saúde"""
    family_members = FamilyMember.objects.all()
    upcoming_appointments = MedicalAppointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')[:5]
    recent_procedures = MedicalProcedure.objects.all().order_by('-procedure_date')[:5]
    
    context = {
        'page_title': 'Dashboard',
        'family_members': family_members,
        'upcoming_appointments': upcoming_appointments,
        'recent_procedures': recent_procedures,
    }
    return render(request, 'healthcare/dashboard.html', context)

@login_required
def family_member_list(request):
    """Lista todos os membros da família"""
    members = FamilyMember.objects.all()
    context = {
        'page_title': 'Membros da Família',
        'members': members
    }
    return render(request, 'healthcare/family_member_list.html', context)

@login_required
def family_member_detail(request, pk):
    """Detalhes de um membro específico da família"""
    member = get_object_or_404(FamilyMember, pk=pk)
    appointments = MedicalAppointment.objects.filter(family_member=member)
    procedures = MedicalProcedure.objects.filter(family_member=member)
    medications = Medication.objects.filter(family_member=member).order_by('-created_at')
    
    context = {
        'page_title': f'Detalhes de {member.name}',
        'member': member,
        'appointments': appointments,
        'procedures': procedures,
        'medications': medications,
    }
    return render(request, 'healthcare/family_member_detail.html', context)

@login_required
def family_member_create(request):
    """Cria um novo membro da família"""
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, 'Membro da família cadastrado com sucesso!')
            return redirect('healthcare:family_member_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FamilyMemberForm()
    
    context = {
        'page_title': 'Novo Membro da Família',
        'form': form
    }
    return render(request, 'healthcare/family_member_form.html', context)

@login_required
def family_member_edit(request, pk):
    """Edita um membro da família existente"""
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro da família atualizado com sucesso!')
            return redirect('healthcare:family_member_detail', pk=pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FamilyMemberForm(instance=member)
        # Formata a data para o formato HTML5 date input
        if member.birth_date:
            form.initial['birth_date'] = member.birth_date.strftime('%Y-%m-%d')
    
    context = {
        'page_title': f'Editar {member.name}',
        'form': form
    }
    return render(request, 'healthcare/family_member_form.html', context)

@login_required
def appointment_list(request):
    """Lista todas as consultas médicas"""
    appointments = MedicalAppointment.objects.all().order_by('-appointment_date')
    context = {
        'page_title': 'Consultas Médicas',
        'appointments': appointments
    }
    return render(request, 'healthcare/appointment_list.html', context)

@login_required
def appointment_create(request):
    """Cria uma nova consulta médica"""
    if request.method == 'POST':
        form = MedicalAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta médica registrada com sucesso!')
            return redirect('healthcare:appointment_list')
    else:
        form = MedicalAppointmentForm()
        if 'family_member' in request.GET:
            form.fields['family_member'].initial = request.GET['family_member']
    
    context = {
        'page_title': 'Nova Consulta',
        'form': form
    }
    return render(request, 'healthcare/appointment_form.html', context)

@login_required
def appointment_edit(request, pk):
    """Edita uma consulta médica existente"""
    appointment = get_object_or_404(MedicalAppointment, pk=pk)
    if request.method == 'POST':
        form = MedicalAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta médica atualizada com sucesso!')
            return redirect('healthcare:appointment_list')
    else:
        initial_data = {
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%dT%H:%M') if appointment.appointment_date else None,
            'next_appointment': appointment.next_appointment.strftime('%Y-%m-%dT%H:%M') if appointment.next_appointment else None,
        }
        form = MedicalAppointmentForm(instance=appointment, initial=initial_data)
    
    context = {
        'page_title': 'Editar Consulta',
        'form': form
    }
    return render(request, 'healthcare/appointment_form.html', context)

@login_required
def procedure_list(request):
    """Lista todos os procedimentos médicos"""
    procedures = MedicalProcedure.objects.all().order_by('-procedure_date')
    context = {
        'page_title': 'Procedimentos Médicos',
        'procedures': procedures
    }
    return render(request, 'healthcare/procedure_list.html', context)

@login_required
def procedure_create(request):
    """Cria um novo procedimento médico"""
    if request.method == 'POST':
        form = MedicalProcedureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Procedimento médico registrado com sucesso!')
            return redirect('healthcare:procedure_list')
    else:
        form = MedicalProcedureForm()
        if 'family_member' in request.GET:
            form.fields['family_member'].initial = request.GET['family_member']
    
    context = {
        'page_title': 'Novo Procedimento',
        'form': form
    }
    return render(request, 'healthcare/procedure_form.html', context)

@login_required
def procedure_edit(request, pk):
    """Edita um procedimento médico existente"""
    procedure = get_object_or_404(MedicalProcedure, pk=pk)
    if request.method == 'POST':
        form = MedicalProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Procedimento médico atualizado com sucesso!')
            return redirect('healthcare:procedure_list')
    else:
        initial_data = {
            'procedure_date': procedure.procedure_date.strftime('%Y-%m-%dT%H:%M') if procedure.procedure_date else None,
            'next_procedure_date': procedure.next_procedure_date.strftime('%Y-%m-%dT%H:%M') if procedure.next_procedure_date else None,
        }
        form = MedicalProcedureForm(instance=procedure, initial=initial_data)
    
    context = {
        'page_title': 'Editar Procedimento',
        'form': form
    }
    return render(request, 'healthcare/procedure_form.html', context)

@login_required
def medication_list(request):
    medications = Medication.objects.all().order_by('-created_at')
    context = {
        'page_title': 'Medicamentos',
        'medications': medications
    }
    return render(request, 'healthcare/medication_list.html', context)

@login_required
def medication_create(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()
            messages.success(request, 'Medicamento registrado com sucesso!')
            return redirect('healthcare:medication_detail', pk=medication.pk)
    else:
        form = MedicationForm()
        if 'family_member' in request.GET:
            form.fields['family_member'].initial = request.GET['family_member']
    
    context = {
        'page_title': 'Novo Medicamento',
        'form': form
    }
    return render(request, 'healthcare/medication_form.html', context)

@login_required
def medication_edit(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            medication = form.save()
            messages.success(request, 'Medicamento atualizado com sucesso!')
            return redirect('healthcare:medication_detail', pk=medication.pk)
    else:
        initial_data = {
            'start_date': medication.start_date.strftime('%Y-%m-%d') if medication.start_date else None,
            'end_date': medication.end_date.strftime('%Y-%m-%d') if medication.end_date else None,
        }
        form = MedicationForm(instance=medication, initial=initial_data)
    
    context = {
        'page_title': 'Editar Medicamento',
        'form': form
    }
    return render(request, 'healthcare/medication_form.html', context)

@login_required
def medication_detail(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    context = {
        'page_title': f'Detalhes do Medicamento - {medication.name}',
        'medication': medication
    }
    return render(request, 'healthcare/medication_detail.html', context)
