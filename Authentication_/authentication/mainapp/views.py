from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required    #tal
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'section':'dashboard'})