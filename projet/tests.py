from django.test import TestCase

# Create your tests here.
def cree_projet(request):
    return render(request, 'acceuil/acceuil.html')
