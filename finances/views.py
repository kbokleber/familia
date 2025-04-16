from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    """Renderiza o dashboard financeiro do Looker Studio."""
    return render(request, 'finances/dashboard.html')
