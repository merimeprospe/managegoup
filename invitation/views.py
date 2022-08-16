from django.shortcuts import render

# Create your views here.

def invitation(request):
    return render(request, 'acceuil/acceuil.html')
