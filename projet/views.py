from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import Notification
# Create your views here.
def cree_projet(request):
    return render(request, 'acceuil/acceuil.html')




#-------------------------------------notification---------------------------------------------------------------

def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    return {'notifications': notifications}


def DeleteNotication(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('projet/projet.html')


def countNotication(request):
    user = request.user
    count_notications = 0
    if request.user.is_authenticated:
        count_notications = Notification.objects.filter(user=user, is_seen=False).count()

    return {'count_notications': count_notications}