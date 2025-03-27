from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('dashboard:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Login realizado com sucesso!')
        return response

class CustomLogoutView(LogoutView):
    next_page = 'accounts:login'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Logout realizado com sucesso!')
        return response

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')

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

def is_admin(user):
    return user.is_superuser

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = get_user_model()
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return is_admin(self.request.user)

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário criado com sucesso!')
        return response

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return response

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return is_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Usuário excluído com sucesso!')
        return response 