from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication, ProcedureDocument
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
    medications = Medication.objects.all().order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Dashboard',
        'family_members': family_members,
        'upcoming_appointments': upcoming_appointments,
        'recent_procedures': recent_procedures,
        'medications': medications,
    }
    return render(request, 'healthcare/dashboard.html', context)

@login_required
def family_member_list(request):
    """Lista todos os membros da família"""
    members = FamilyMember.objects.all()
    context = {
        'page_title': 'Membros da Família',
        'family_members': members
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
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, 'Membro da família cadastrado com sucesso!')
            return redirect('healthcare:family_member_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FamilyMemberForm()
    
    context = {
        'page_title': 'Novo Membro da Família',
        'form': form,
        'model_name': 'Membro da Família',
        'list_url': reverse('healthcare:family_member_list')
    }
    return render(request, 'healthcare/family_member_form.html', context)

@login_required
def family_member_edit(request, pk):
    """Edita um membro da família"""
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro da família atualizado com sucesso!')
            return redirect('healthcare:family_member_list')
    else:
        form = FamilyMemberForm(instance=member)
    
    context = {
        'page_title': 'Editar Membro da Família',
        'form': form,
        'model_name': 'Membro da Família',
        'list_url': reverse('healthcare:family_member_list')
    }
    return render(request, 'healthcare/family_member_form.html', context)

@login_required
def family_member_delete(request, pk):
    """Exclui um membro da família"""
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Membro da família excluído com sucesso!')
        return redirect('healthcare:family_member_list')
    return redirect('healthcare:family_member_list')

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
        'form': form,
        'model_name': 'Consulta',
        'list_url': reverse('healthcare:appointment_list')
    }
    return render(request, 'healthcare/appointment_form.html', context)

@login_required
def appointment_edit(request, pk):
    """Edita uma consulta médica"""
    appointment = get_object_or_404(MedicalAppointment, pk=pk)
    if request.method == 'POST':
        form = MedicalAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta médica atualizada com sucesso!')
            return redirect('healthcare:appointment_list')
    else:
        form = MedicalAppointmentForm(instance=appointment)
    
    context = {
        'page_title': 'Editar Consulta',
        'form': form,
        'model_name': 'Consulta',
        'list_url': reverse('healthcare:appointment_list')
    }
    return render(request, 'healthcare/appointment_form.html', context)

@login_required
def appointment_delete(request, pk):
    """Exclui uma consulta médica"""
    appointment = get_object_or_404(MedicalAppointment, pk=pk)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Consulta médica excluída com sucesso!')
        return redirect('healthcare:appointment_list')
    
    return redirect('healthcare:appointment_list')

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
        form = MedicalProcedureForm(request.POST, request.FILES)
        if form.is_valid():
            procedure = form.save()
            
            # Processa os arquivos enviados
            files = request.FILES.getlist('documents')
            for file in files:
                ProcedureDocument.objects.create(
                    procedure=procedure,
                    file=file,
                    name=file.name
                )
            
            messages.success(request, 'Procedimento médico registrado com sucesso!')
            return redirect('healthcare:procedure_list')
    else:
        form = MedicalProcedureForm()
        if 'family_member' in request.GET:
            form.fields['family_member'].initial = request.GET['family_member']
    
    context = {
        'page_title': 'Novo Procedimento',
        'form': form,
        'model_name': 'Procedimento',
        'list_url': reverse('healthcare:procedure_list')
    }
    return render(request, 'healthcare/procedure_form.html', context)

@login_required
def procedure_edit(request, pk):
    """Edita um procedimento médico"""
    procedure = get_object_or_404(MedicalProcedure, pk=pk)
    if request.method == 'POST':
        form = MedicalProcedureForm(request.POST, request.FILES, instance=procedure)
        if form.is_valid():
            form.save()
            
            # Processa os arquivos enviados
            files = request.FILES.getlist('documents')
            for file in files:
                ProcedureDocument.objects.create(
                    procedure=procedure,
                    file=file,
                    name=file.name
                )
            
            messages.success(request, 'Procedimento médico atualizado com sucesso!')
            return redirect('healthcare:procedure_list')
    else:
        form = MedicalProcedureForm(instance=procedure)
    
    context = {
        'page_title': 'Editar Procedimento',
        'form': form,
        'model_name': 'Procedimento',
        'list_url': reverse('healthcare:procedure_list')
    }
    return render(request, 'healthcare/procedure_form.html', context)

@login_required
def procedure_delete(request, pk):
    """Exclui um procedimento médico"""
    procedure = get_object_or_404(MedicalProcedure, pk=pk)
    
    if request.method == 'POST':
        procedure.delete()
        messages.success(request, 'Procedimento médico excluído com sucesso!')
        return redirect('healthcare:procedure_list')
    
    return redirect('healthcare:procedure_list')

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
    """Cria um novo medicamento"""
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
        'form': form,
        'model_name': 'Medicamento',
        'list_url': reverse('healthcare:medication_list')
    }
    return render(request, 'healthcare/medication_form.html', context)

@login_required
def medication_edit(request, pk):
    """Edita um medicamento"""
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento atualizado com sucesso!')
            return redirect('healthcare:medication_detail', pk=medication.pk)
    else:
        form = MedicationForm(instance=medication)
    
    context = {
        'page_title': 'Editar Medicamento',
        'form': form,
        'model_name': 'Medicamento',
        'list_url': reverse('healthcare:medication_list')
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
