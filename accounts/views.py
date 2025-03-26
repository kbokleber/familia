from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import redirect

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = ProfileForm()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = ProfileForm(self.request.POST, instance=self.object.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return response

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('dashboard:home')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = ProfileForm(self.request.POST, instance=self.request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Perfil atualizado com sucesso!')
        return response

class SettingsView(LoginRequiredMixin, SuperUserRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-date_joined')
        return context

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action', request.POST.get('action'))
        
        if action == 'create_user':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password1 != password2:
                messages.error(request, 'As senhas não coincidem.')
                return redirect('accounts:settings')

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, f'Usuário {username} criado com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')

        elif action == 'update_user':
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                user.email = request.POST.get('email')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.is_active = request.POST.get('is_active') == 'on'
                user.save()
                messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar usuário: {str(e)}')

        elif action == 'delete_user':
            user_id = kwargs.get('pk')
            try:
                user = User.objects.get(id=user_id)
                if user != request.user:
                    username = user.username
                    user.delete()
                    messages.success(request, f'Usuário {username} excluído com sucesso!')
                else:
                    messages.error(request, 'Você não pode excluir seu próprio usuário.')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao excluir usuário: {str(e)}')

        return redirect('accounts:settings') 