import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from personne.form import EditProfileForm
from projet.models import Project, Partenaire, Carte, Notification, Tache, Log
from projet.form import projetform, carteform, partenaireform, notifform, descriptionform, tacheform
from personne.models import Profile, Account
from django.contrib import messages

# Create your views here.

@login_required
def profile(request, id):
    user = request.user
    profile = Profile.objects.get(user=user)
    # ------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()

    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    # ----------------------fin_notif----------------------------
    if request.method == "POST":
        form = EditProfileForm(request.POST,  request.FILES)
        if form.is_valid():
            p = form.cleaned_data.get('picture')
            if p:
                profile.picture = p
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.localisationtion = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('profile', id)
    else:
        form = EditProfileForm()

    context = {'form': form, 'profile': profile, 'count_notications': count_notications, 'notifications': notifications}
    return render(request, 'compte/profile.html', context)


@login_required
def notif(request):
    user = request.user
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#--------------------------------------Espace de travail--------------------------------------------------
@login_required
def espace(request):
    # recherche
    user = request.user

    # lister
    partenaire = []
    # ------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()

    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')

    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    # ----------------------fin_notif----------------------------
    projet = Project.objects.filter(user=user)
    projet1 = Partenaire.objects.filter(user=user,is_active=True)
    j = 0
    i = 0
    k = 0
    y = 0
    for p in projet:
        i = i + 1
        partenaire1 = Partenaire.objects.filter(project=p.id)
        for pt in partenaire1:
            k = k + 1
            partenaire.append(pt.id)
            print(partenaire)
        cartes = Carte.objects.filter(project=p.id)
        for pt in cartes:
            y = y + 1

    partenaire1 = Partenaire.objects.filter(id__in=partenaire,is_active=True).all()

    for p in projet1:
        j = j + 1
    profile = Profile.objects.get(user=user)

    # ajouter
    form = projetform(request.POST, request.FILES)
    if request.method == 'POST':
        form = projetform(request.POST, request.FILES)
        if form.is_valid():
            print("111111111111111111")
            order = form.save(commit=False)
            try:
                projt = Project.objects.get(theme=order.theme, user=request.user)
                messages.error(request, " Un projet de ce nom existe déja ")
            except:
                order.user = request.user
                order.save()
                carte1 = Carte()
                carte1.nom_carte = 'A faire'
                carte1.project = order
                carte1.save()
                carte2 = Carte()
                carte2.nom_carte = 'Terminer'
                carte2.project = order
                carte2.save()
                return redirect('espace')

    listes = Project.objects.filter(user=user)
    recherche = request.GET.get('recherche')
    if recherche != '' and recherche is not None:
        listes = Project.objects.filter(theme=recherche)
        print(listes)
        context1 = {'listes': listes, 'count_notications': count_notications, 'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet, 'form': form, 'profile': profile,
               'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y}
        return render(request, 'compte/recherche.html', context1)

    context = {'count_notications': count_notications, 'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet, 'form': form, 'profile': profile,
               'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y}
    return render(request, 'compte/espace.html', context)

#----------------------------------------
@login_required
def carte(request):
    # recherche
    user = request.user

    # lister
    partenaire = []
    # ------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()

    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    # ----------------------fin_notif----------------------------
    carte = []
    projet = Project.objects.filter(user=user)
    projet1 = Partenaire.objects.filter(user=user, is_active=True)
    j = 0
    i = 0
    k = 0
    y = 0
    for p in projet:
        i = i + 1
        partenaire1 = Partenaire.objects.filter(project=p.id, is_active=True)
        for pt in partenaire1:
            k = k + 1
            partenaire.append(pt.id)
            print(partenaire)
        cartes = Carte.objects.filter(project=p.id)
        for pt in cartes:
            y = y + 1
            carte.append(pt.id)
    cartes = Carte.objects.filter(id__in=carte).all
    partenaire1 = Partenaire.objects.filter(id__in=partenaire, is_active=True).all()

    for p in projet1:
        j = j + 1
    profile = Profile.objects.get(user=user)

    listes = Project.objects.filter(user=user)
    recherche = request.GET.get('recherche')
    if recherche != '' and recherche is not None:
        listes = Project.objects.filter(theme=recherche)
        print(listes)
        context1 = {'listes': listes, 'count_notications': count_notications, 'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet, 'profile': profile,
               'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y, 'cartes': cartes}
        return render(request, 'compte/recherche.html', context1)

    context = {'count_notications': count_notications, 'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet, 'profile': profile,
               'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y, 'cartes': cartes}
    return render(request, 'compte/cartes.html', context)


#---------------------------------------aide-----------------------------------------------------------
@login_required
def aide(request):
    user = request.user
    # ------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()

    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    # ----------------------fin_notif----------------------------
    profile = Profile.objects.get(user=user)

    listes = Project.objects.filter(user=user)
    recherche = request.GET.get('recherche')
    if recherche != '' and recherche is not None:
        listes = Project.objects.filter(theme=recherche)
        print(listes)
        context1 = {'listes': listes, 'count_notications': count_notications, 'notifications': notifications, 'profile': profile}
        return render(request, 'compte/recherche.html', context1)

    context = {'count_notications': count_notications, 'notifications': notifications, 'profile': profile}
    return render(request, 'compte/Aide.html', context)

#---------------------------------------acceuil adminitrateur---------------------------------------------------
@login_required
def adminDashboard1(request):
    return render(request, 'compte/Dashboard1.html')


#---------------------------------------acceuil utilisateur---------------------------------------------------

@login_required
def adminDashboard2(request):
    user = request.user

    #lister
    partenaire = []

        #------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()

    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')

    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

        #----------------------fin_notif----------------------------

    projet = Project.objects.filter(user=user)
    projet1 = Partenaire.objects.filter(user=user, is_active=True)
    j = 0
    i = 0
    k = 0
    y = 0
    sup = 0
    mod = 0
    cre = 0
    for p in projet:
        i = i + 1
        log = Log.objects.filter(user_projet=p).order_by('-date_creation')
        for l in log:
            if l.types_log == 1:
                cre = cre + 1
            if l.types_log == 2:
                sup = sup + 1
            if l.types_log == 3:
                mod = mod + 1

        partenaire1 = Partenaire.objects.filter(project=p.id, is_active=True)
        for pt in partenaire1:
            k = k + 1
            partenaire.append(pt.id)
            print(partenaire)
        cartes = Carte.objects.filter(project=p.id)
        for pt in cartes:
            taches = Tache.objects.filter(carte=pt.id)
            for pd in taches:
                y = y+1

    partenaire1 = Partenaire.objects.filter(id__in=partenaire, is_active=True).all()

    for p in projet1:
        j = j + 1

    profile = Profile.objects.get(user=user)

    # recherche
    listes = Project.objects.filter(user=user)
    recherche = request.GET.get('recherche')
    if recherche != '' and recherche is not None:
        listes = Project.objects.filter(theme=recherche)
        print(listes)
        context1 = {'listes': listes, 'sup': sup, 'mod': mod, 'cre': cre, 'count_notications': count_notications,
                   'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet,
                   'profile': profile, 'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y}
        return render(request, 'compte/recherche.html', context1)

    context = {'sup': sup, 'mod': mod, 'cre': cre, 'count_notications': count_notications,
               'notifications': notifications, 'liste': listes, 'partenaire': partenaire1, 'projet': projet,
               'profile': profile, 'projet1': projet1, 'i': i, 'j': j, 'k': k, 'y': y}
    return render(request, 'compte/Dashboard2.html', context)


#---------------------------------------parge projet---------------------------------------------------
@login_required
def projet(request, id):
    user = request.user
    profile = Profile.objects.get(user=user)
    projet = Project.objects.get(id=id)
    log = Log.objects.filter(user_projet=id).order_by('-date_creation')
    print(profile.picture)

    # ------------------notification----------------------------

    count_notications = Notification.objects.filter(sender=user, is_seen=False).count()
    notifications = Notification.objects.filter(sender=user).order_by('-date_creation')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    # ----------------------fin_notif----------------------------

    # ajouter
    #------------------------tache---------------------------------

    form3 = tacheform(request.POST, request.FILES)
    if request.method == 'POST':
        form3 = tacheform(request.POST, request.FILES)
        if form3.is_valid():
            order = form3.save(commit=False)
            email = request.POST.get('email1')
            carte1 = Carte.objects.get(project=projet, nom_carte='A faire')
            try:
                user_p = Account.objects.get(email=email)
                try:
                    tache_P = Tache.objects.get(nom_tache=order.nom_tache, projet=projet, carte=carte1)
                    messages.error(request, " La tache existe deja")
                except:
                    try:
                        if(user != user_p):
                            print(111111111111111)
                            parte = Partenaire.objects.get(user=user_p, project=projet)
                            print(111111111111111)

                        order.user = user_p
                        order.projet = projet
                        order.carte = carte1
                        order.save()

                        log = Log()
                        log.user_projet = projet
                        log.user_log = user
                        log.contenue_log = 'la tache '+order.nom_tache
                        log.types_log = 1
                        log.save()
                    except:
                        messages.error(request, " L'utilisateur n'a partient par au projet ")

            except:
                messages.error(request, " l'utilisateur n'existe pas ")

            return redirect('projet', id)

                #-------------------------------------modif-------------------------
    #-----------------------Carte-------------------------------------
    form = carteform(request.POST, request.FILES)
    if request.method == 'POST':
        form = carteform(request.POST, request.FILES)
        if form.is_valid():
            print("111111111111111111")
            order = form.save(commit=False)
            order.project = projet
            try:
                carte_P = Carte.objects.get(nom_carte=order.nom_carte, project=projet)
                messages.error(request, " La carte existe deja")
            except:
                order.save()

                log = Log()
                log.user_projet = projet
                log.user_log = user
                log.contenue_log = 'la carte ' + order.nom_carte
                log.types_log = 1
                log.save()

            return redirect('projet', id)

    # -----------------------partenaire-------------------------------------
    form1 = partenaireform(request.POST, request.FILES)
    if request.method == 'POST':
        form1 = partenaireform(request.POST, request.FILES)
        print(55555555555555555555555555)
        if form1.is_valid():
            print(55555555555555555555555555)
            order = form1.save(commit=False)
            email = request.POST.get('email')
            order.designation = request.POST.get('designation')
            try:
                user_p = Account.objects.get(email=email)
                try:
                    Partenaire.objects.get(user=user_p, project=projet)
                    messages.error(request, " l'utilisateur appartient deje au projet")
                except:
                    print(9999999999999)
                    if user == user_p:
                        messages.error(request, " vous ne pouvez pas etre partenaire de votre propre projet ")
                    else:
                        order.user = user_p
                        order.project = projet
                        order.save()

                        log = Log()
                        log.user_projet = projet
                        log.user_log = user
                        log.contenue_log = " l'utilisateur " + user_p.username
                        log.types_log = 1
                        log.save()

                        # -----------------------notif----------------------------
                        notyf = Notification()
                        notyf.user = user
                        notyf.sender = user_p
                        notyf.project = projet
                        notyf.notification = 1
                        notyf.is_seen = False
                        notyf.save()
                    return redirect('projet', id)
            except:
                messages.error(request, " l'utilisateur n'existe pas ")
            return redirect('projet', id)
            print(email)
    tache = Tache.objects.filter(projet=projet)
    partenaires = Partenaire.objects.filter(project=id, is_active=True)
    carte = Carte.objects.filter(project=id)

    context = {'tache': tache, 'log': log, 'profile': profile, 'partenaires': partenaires, 'form3': form3, 'form': form, 'form1': form1, 'carte': carte, 'projet': projet, 'notifications': notifications, 'count_notications': count_notications}
    return render(request, 'projet/projet.html', context)


#-------------------------------supprimer----------------------------------------------------------------

@login_required
def delet_p(request, id):
    sup = Project.objects.filter(id=id).delete()
    return redirect('adminDashboard2')

@login_required
def delet_a(request, id):
    sup = Partenaire.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " son driot d'accet au projet "
    log.types_log = 2
    log.save()
    sup.delete()
    return redirect('adminDashboard2')

@login_required
def supp(request, id):
    sup = Carte.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " la carte " + sup.nom_carte
    log.types_log = 2
    log.save()
    sup.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def supp_t(request, id):
    print(11111111111111111)
    sup = Tache.objects.get(id=id)
    projet = Project.objects.get(id=sup.projet.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " la tache " + sup.nom_tache
    log.types_log = 2
    log.save()
    sup.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delet_ap(request, id,pk):
    sup = Partenaire.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " l'utilisateur du projet " + sup.user.username
    log.types_log = 2
    log.save()
    sup.delete()
    return redirect('projet', pk)

@login_required
def supp1(request, id,pk):
    print(11111111111111111)
    sup = Carte.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " la carte " + sup.nom_carte
    log.types_log = 2
    log.save()
    sup.delete()
    return redirect('projet', pk)

@login_required
def delet_p1(request, id):
    sup = Project.objects.get(id=id).delete()
    return redirect('espace')

@login_required
def delet_a1(request, id):
    sup = Partenaire.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " l'utilisateur du projet " + sup.user.username
    log.types_log = 2
    log.save()
    sup.delete()
    return redirect('espace')

@login_required
def delet_p2(request, id):
    sup = Project.objects.filter(id=id).delete()
    return redirect('carte')

@login_required
def delet_a2(request, id):
    sup = Partenaire.objects.get(id=id)
    projet = Project.objects.get(id=sup.project.id)
    user = request.user
    log = Log()
    log.user_projet = projet
    log.user_log = user
    log.contenue_log = " l'utilisateur du projet " + sup.user.username
    log.types_log = 2
    log.save()
    sup.delete()
    return redirect('carte')

#-------------------------------delet notyf-----------------------------------
@login_required
def delet_np(request, id,):
    sup = Notification.objects.filter(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delet_n(request, id, pk):
    user = request.user
    notyf1 = Notification.objects.get(id=id)
    sup = Notification.objects.filter(id=id).delete()
    Partenaire.objects.filter(user=user, project=pk, is_active=False).update(is_active=True)
    notyf = Notification()
    notyf.user = user
    notyf.sender = notyf1.user
    notyf.project = notyf1.project
    notyf.notification = 2
    notyf.is_seen = False
    notyf.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delet_no(request, id, pk):

    user = request.user
    notyf1 = Notification.objects.get(id=id)
    sup = Notification.objects.filter(id=id).delete()
    sup1 = Partenaire.objects.filter(user=user, project=pk, is_active=False).delete()
    notyf = Notification()
    notyf.user = user
    notyf.sender = notyf1.user
    notyf.project = notyf1.project
    notyf.notification = 3
    notyf.is_seen = False
    notyf.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#-------------------------------madifier------------------------------------------------------------------

@login_required
def modif_p(request, id):

    modify = Project.objects.get(id=id)
    form = projetform(instance=modify)
    if request.method == "POST":
        form = projetform(request.POST, instance=modify)
        if form.is_valid():
            form.save()
            projet = Project.objects.get(id=id)
            user = request.user
            log = Log()
            log.user_projet = projet
            log.user_log = user
            log.contenue_log = " le theme du projet pas " + projet.theme
            log.types_log = 3
            log.save()
            print(111111)
        return redirect('espace')
    context = {'form': form}

    return render(request, 'compte/espace.html', context)

def modif_t(request, id):
    modify = Tache.objects.get(id=id)
    if request.method == "POST":
        carte = request.POST.get('carte')
        try:
            cart = Carte.objects.get(nom_carte=carte, project=modify.projet)
            new_tache = Tache()
            new_tache.nom_tache = modify.nom_tache
            new_tache.user = modify.user
            new_tache.carte = cart
            new_tache.projet = modify.projet
            new_tache.save()
            user = request.user
            log = Log()
            log.user_projet = modify.projet
            log.user_log = user
            log.contenue_log = " la carte de la tache "+modify.nom_tache+" pas " + cart.nom_carte
            log.types_log = 3
            log.save()
            modify.delete()

        except:
            messages.error(request, " la carte "+carte+" "+"n'esiste pas")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def modif_t_d(request, id):
    modify = Tache.objects.get(id=id)
    if request.method == "POST":
        d = request.POST.get('decision')
        new_tache = Tache()
        new_tache.nom_tache = modify.nom_tache
        new_tache.user = modify.user
        new_tache.carte = modify.carte
        new_tache.projet = modify.projet
        new_tache.decision = d
        new_tache.save()
        modify.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def views_tache_by_id(request, tache_id):
    tache = Tache.objects.filter(id=tache_id).values()
    tach = json.dumps(list(tache), cls=DjangoJSONEncoder)
    return JsonResponse(tach, safe=False)