from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
import django
import sys
from django.conf import settings

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

class SettingsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/settings.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['django_version'] = django.get_version()
        context['python_version'] = sys.version.split()[0]
        context['environment'] = 'Desenvolvimento' if settings.DEBUG else 'Produção'
        context['debug'] = settings.DEBUG
        context['database'] = 'SQLite' if settings.DEBUG else 'PostgreSQL'
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'create':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuário criado com sucesso!')
            else:
                messages.error(request, 'Erro ao criar usuário. Verifique os dados.')
        elif action == 'update' and user_id:
            user = get_object_or_404(User, id=user_id)
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuário atualizado com sucesso!')
            else:
                messages.error(request, 'Erro ao atualizar usuário. Verifique os dados.')
        elif action == 'delete' and user_id:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'Usuário excluído com sucesso!')

        return redirect('accounts:settings')

def is_admin(user):
    return user.is_superuser

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário criado com sucesso!')
        return response

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Usuário excluído com sucesso!')
        return response

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form': form}) 