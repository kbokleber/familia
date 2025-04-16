from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SystemConfig
from .forms import SystemConfigForm

@login_required
def system_config_list(request):
    """Lista todas as configurações do sistema"""
    configs = SystemConfig.objects.all()
    
    if request.method == 'POST':
        form = SystemConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuração adicionada com sucesso!')
            return redirect('core:system_config_list')
    else:
        form = SystemConfigForm()
    
    context = {
        'page_title': 'Configurações do Sistema',
        'configs': configs,
        'form': form
    }
    return render(request, 'core/system_config_list.html', context)

@login_required
def system_config_edit(request, pk):
    """Edita uma configuração do sistema"""
    config = get_object_or_404(SystemConfig, pk=pk)
    
    if request.method == 'POST':
        form = SystemConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuração atualizada com sucesso!')
            return redirect('core:system_config_list')
    else:
        form = SystemConfigForm(instance=config)
    
    context = {
        'page_title': 'Editar Configuração',
        'form': form,
        'config': config
    }
    return render(request, 'core/system_config_form.html', context)

@login_required
def system_config_delete(request, pk):
    """Exclui uma configuração do sistema"""
    config = get_object_or_404(SystemConfig, pk=pk)
    
    if request.method == 'POST':
        config.delete()
        messages.success(request, 'Configuração excluída com sucesso!')
    
    return redirect('core:system_config_list') 