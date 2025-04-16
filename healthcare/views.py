from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication, ProcedureDocument, AppointmentDocument, MedicationDocument, Exam
from .forms import FamilyMemberForm, MedicalAppointmentForm, MedicalProcedureForm, MedicationForm, ExamForm
from django.utils import timezone
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db import transaction

@login_required
def healthcare_dashboard(request):
    """Dashboard principal do sistema de saúde"""
    # Buscar todos os membros da família
    family_members = FamilyMember.objects.all()

    # Contadores
    appointments_count = MedicalAppointment.objects.count()
    procedures_count = MedicalProcedure.objects.count()
    medications_count = Medication.objects.count()
    exams_count = Exam.objects.count()

    # Próximas consultas
    upcoming_appointments = MedicalAppointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')[:5]

    # Dados do gráfico (últimos 12 meses)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    
    # Dados de procedimentos
    procedures_data = MedicalProcedure.objects.filter(
        procedure_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('procedure_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Dados de consultas
    appointments_data = MedicalAppointment.objects.filter(
        appointment_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('appointment_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Dados de medicamentos
    medications_data = Medication.objects.filter(
        start_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('start_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Dados de exames
    exams_data = Exam.objects.filter(
        exam_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('exam_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Preparar dados para o gráfico
    chart_labels = []
    procedures_chart_data = []
    appointments_chart_data = []
    medications_chart_data = []
    exams_chart_data = []
    
    current_date = start_date
    while current_date <= end_date:
        month_label = current_date.strftime('%b/%Y')
        chart_labels.append(month_label)
        
        # Encontrar os valores para este mês
        month_procedures = next(
            (item['count'] for item in procedures_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        procedures_chart_data.append(month_procedures)

        month_appointments = next(
            (item['count'] for item in appointments_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        appointments_chart_data.append(month_appointments)

        month_medications = next(
            (item['count'] for item in medications_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        medications_chart_data.append(month_medications)

        month_exams = next(
            (item['count'] for item in exams_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        exams_chart_data.append(month_exams)
        
        current_date += timedelta(days=32)  # Avançar para o próximo mês

    context = {
        'page_title': 'Dashboard',
        'family_members': family_members,
        'upcoming_appointments': upcoming_appointments,
        'appointments_count': appointments_count,
        'procedures_count': procedures_count,
        'medications_count': medications_count,
        'exams_count': exams_count,
        'chart_labels': chart_labels,
        'procedures_chart_data': procedures_chart_data,
        'appointments_chart_data': appointments_chart_data,
        'medications_chart_data': medications_chart_data,
        'exams_chart_data': exams_chart_data,
    }
    return render(request, 'healthcare/dashboard.html', context)

@login_required
def family_member_list(request):
    """Lista todos os membros da família"""
    members = FamilyMember.objects.all().order_by('order', 'name')
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
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                print(f"Processando foto: {photo_file.name}, tamanho: {photo_file.size} bytes")
                member.set_photo(photo_file)
                if member.photo:
                    print(f"Foto salva com sucesso. Tamanho após processamento: {len(member.photo)} bytes")
                else:
                    print("Erro: Foto não foi salva corretamente")
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
            member = form.save(commit=False)
            
            # Verifica se deve limpar a foto
            if request.POST.get('clear_photo') == 'true':
                member.photo = None
                member.photo_type = None
                print("[DEBUG] Removendo foto do membro")
            # Se não deve limpar, processa a nova foto se foi enviada
            elif 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                print(f"[DEBUG] Recebendo foto no POST: {photo_file.name}, tamanho: {photo_file.size} bytes")
                print(f"[DEBUG] Tipo MIME: {photo_file.content_type}")
                
                # Processa a foto
                success = member.set_photo(photo_file)
                if success:
                    print(f"[DEBUG] Foto processada com sucesso. Tamanho: {len(member.photo)} bytes, Tipo: {member.photo_type}")
                else:
                    print("[ERROR] Falha ao processar a foto")
                    messages.error(request, 'Erro ao processar a foto. Por favor, tente novamente.')
                    return redirect('healthcare:family_member_edit', pk=pk)
            
            try:
                member.save()
                print("[DEBUG] Membro da família salvo com sucesso")
                messages.success(request, 'Membro da família atualizado com sucesso!')
                return redirect('healthcare:family_member_list')
            except Exception as e:
                print(f"[ERROR] Erro ao salvar membro da família: {str(e)}")
                messages.error(request, 'Erro ao salvar as alterações. Por favor, tente novamente.')
                return redirect('healthcare:family_member_edit', pk=pk)
        else:
            print("[DEBUG] Formulário inválido:", form.errors)
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        initial_data = {
            'birth_date': member.birth_date.strftime('%Y-%m-%d') if member.birth_date else None
        }
        form = FamilyMemberForm(instance=member, initial=initial_data)
    
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
        form = MedicalAppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save()
            
            # Processa os arquivos enviados
            files = request.FILES.getlist('documents')
            for file in files:
                AppointmentDocument.objects.create(
                    appointment=appointment,
                    file=file,
                    name=file.name
                )
            
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
        form = MedicalAppointmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            
            # Processa os arquivos enviados
            files = request.FILES.getlist('documents')
            for file in files:
                AppointmentDocument.objects.create(
                    appointment=appointment,
                    file=file,
                    name=file.name
                )
            
            messages.success(request, 'Consulta médica atualizada com sucesso!')
            return redirect('healthcare:appointment_list')
    else:
        # Formata as datas para o formato esperado pelo input datetime-local
        initial_data = {
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%dT%H:%M'),
            'next_appointment': appointment.next_appointment.strftime('%Y-%m-%dT%H:%M') if appointment.next_appointment else None
        }
        form = MedicalAppointmentForm(instance=appointment, initial=initial_data)
    
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
    
    return render(request, 'healthcare/procedure_form.html', {
        'form': form,
        'model_name': 'Procedimento',
        'list_url': reverse('healthcare:procedure_list')
    })

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
        # Formata as datas para o formato esperado pelo input datetime-local
        initial_data = {
            'procedure_date': procedure.procedure_date.strftime('%Y-%m-%dT%H:%M'),
            'next_procedure_date': procedure.next_procedure_date.strftime('%Y-%m-%dT%H:%M') if procedure.next_procedure_date else None
        }
        form = MedicalProcedureForm(instance=procedure, initial=initial_data)
    
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
    """Lista todos os medicamentos"""
    medications = Medication.objects.all().select_related('family_member').order_by('-created_at')

    # Preparar dados para o template
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
        form = MedicationForm(request.POST, request.FILES, instance=medication)
        if form.is_valid():
            medication = form.save()
            
            # Processa os arquivos enviados
            files = request.FILES.getlist('documents')
            for file in files:
                MedicationDocument.objects.create(
                    medication=medication,
                    file=file,
                    name=file.name
                )
            
            messages.success(request, 'Medicamento atualizado com sucesso!')
            return redirect('healthcare:medication_list')
    else:
        # Formata as datas para o formato esperado pelo input datetime-local
        initial_data = {}
        if medication.start_date:
            # Converte para o fuso horário local e depois para o formato esperado
            local_start_date = timezone.localtime(medication.start_date)
            initial_data['start_date'] = local_start_date.strftime('%Y-%m-%dT%H:%M')
        if medication.end_date:
            local_end_date = timezone.localtime(medication.end_date)
            initial_data['end_date'] = local_end_date.strftime('%Y-%m-%dT%H:%M')
        
        form = MedicationForm(instance=medication, initial=initial_data)
    
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

@login_required
def medication_delete(request, pk):
    """Exclui um medicamento"""
    medication = get_object_or_404(Medication, pk=pk)
    
    if request.method == 'POST':
        medication.delete()
        messages.success(request, 'Medicamento excluído com sucesso!')
        return redirect('healthcare:medication_list')
    
    return redirect('healthcare:medication_list')

@login_required
def procedures_chart_data(request):
    months = int(request.GET.get('months', 12))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=months * 30)
    
    # Buscar membros da família do usuário
    family_members = FamilyMember.objects.filter(user=request.user)
    
    procedures_data = MedicalProcedure.objects.filter(
        family_member__in=family_members,
        procedure_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('procedure_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Preparar dados para o gráfico
    labels = []
    data = []
    
    current_date = start_date
    while current_date <= end_date:
        month_label = current_date.strftime('%b/%Y')
        labels.append(month_label)
        
        # Encontrar o valor para este mês
        month_data = next(
            (item['count'] for item in procedures_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        data.append(month_data)
        
        current_date += timedelta(days=32)  # Avançar para o próximo mês

    return JsonResponse({
        'labels': labels,
        'data': data
    })

def chart_data(request):
    """View para fornecer dados do gráfico via API"""
    months = int(request.GET.get('months', 12))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30 * months)
    
    # Filtrar membros da família do usuário
    family_members = FamilyMember.objects.filter(user=request.user)
    
    # Consultas
    appointments_data = (
        MedicalAppointment.objects
        .filter(family_member__in=family_members, appointment_date__gte=start_date)
        .annotate(month=TruncMonth('appointment_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Medicamentos
    medications_data = (
        Medication.objects
        .filter(family_member__in=family_members, start_date__gte=start_date)
        .annotate(month=TruncMonth('start_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Procedimentos
    procedures_data = (
        MedicalProcedure.objects
        .filter(family_member__in=family_members, procedure_date__gte=start_date)
        .annotate(month=TruncMonth('procedure_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Exames
    exams_data = (
        Exam.objects
        .filter(family_member__in=family_members, exam_date__gte=start_date)
        .annotate(month=TruncMonth('exam_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Preparar dados para o gráfico
    months_list = []
    appointments_counts = []
    medications_counts = []
    procedures_counts = []
    exams_counts = []
    
    current_date = start_date
    while current_date <= end_date:
        month_str = current_date.strftime('%b/%Y')
        months_list.append(month_str)
        
        # Contagem de consultas
        appointment_count = next(
            (item['count'] for item in appointments_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        appointments_counts.append(appointment_count)
        
        # Contagem de medicamentos
        medication_count = next(
            (item['count'] for item in medications_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        medications_counts.append(medication_count)
        
        # Contagem de procedimentos
        procedure_count = next(
            (item['count'] for item in procedures_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        procedures_counts.append(procedure_count)
        
        # Contagem de exames
        exam_count = next(
            (item['count'] for item in exams_data if item['month'].strftime('%Y-%m') == current_date.strftime('%Y-%m')),
            0
        )
        exams_counts.append(exam_count)
        
        current_date += timedelta(days=30)
    
    return JsonResponse({
        'labels': months_list,
        'appointments_data': appointments_counts,
        'medications_data': medications_counts,
        'procedures_data': procedures_counts,
        'exams_data': exams_counts
    })

@login_required
def save_family_members_order(request):
    """Salva a nova ordem dos membros da família."""
    if request.method == 'POST':
        try:
            member_ids = request.POST.getlist('member_ids[]')
            print(f"[DEBUG] Recebendo nova ordem de membros: {member_ids}")
            
            # Primeiro, verifica se todos os IDs são válidos
            for member_id in member_ids:
                try:
                    FamilyMember.objects.get(pk=member_id)
                except FamilyMember.DoesNotExist:
                    print(f"[ERROR] Membro com ID {member_id} não encontrado")
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Membro com ID {member_id} não encontrado'
                    }, status=400)
            
            # Atualiza a ordem de todos os membros em uma única transação
            with transaction.atomic():
                for index, member_id in enumerate(member_ids):
                    member = FamilyMember.objects.get(pk=member_id)
                    print(f"[DEBUG] Atualizando membro {member.name} (ID: {member_id}) para ordem {index}")
                    member.order = index
                    member.save(update_fields=['order'])
            
            # Verifica a ordem após salvar
            all_members = FamilyMember.objects.all().order_by('order', 'name')
            print("[DEBUG] Ordem atual dos membros após salvar:")
            for member in all_members:
                print(f"[DEBUG] - {member.name}: ordem {member.order}")
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"[ERROR] Erro ao salvar ordem: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao salvar ordem: {str(e)}'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido'
    }, status=405)
