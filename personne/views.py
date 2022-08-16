from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from personne.form import SignupForm, ChangePasswordForm, AccountAuthenticationForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, logout, login
from personne.models import Account, Profile
from django.urls import reverse

from personne.tokens import generate_token
from trello_isj import settings


def acceuil(request):
    return render(request, 'personne/index.html')


def Signup(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == '1':
            return redirect(reverse("adminDashboard1"))
        else:
            return redirect("adminDashboard2")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            myuser = Account.objects.create_user(username=username, email=email, password=password)
            myuser.is_active = False
            myuser.save()

            messages.success(request,
                             "Votre compte a été crée avec succès. Un message de confirmation a été envoyé dans votre boite Email, veillez le confirmer pour activer votre compte")
            # Bienvenue Email

            subject = "Bienvenue dans managegroupe !!"
            message = "Hello " + myuser.username + "!! \n" + "Merci pour avoir choisi SalariApp pour la gestion de vos salaires \nVous allez recevoir un message de confirmation pour activer votre compte. \n\n\n Merci \n Cordialement Managegroupe "
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            print(111333333)

            send_mail(subject, message, from_email, to_list, fail_silently=True)
            print(111111111)

            # Addresse Email de confirmation

            current_site = get_current_site(request)
            email_subject = "Confirmation de l'addresse email"
            domain= get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(myuser.id))
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': generate_token.make_token(myuser)
            })
            activate_url = 'http://'+domain+link
            message2 = 'hi'+myuser.username + \
                'veuillez utiliser ce lien pour vérifier votre compte\n' + activate_url
            email = EmailMessage(
                 email_subject,
                 message2,
                 settings.EMAIL_HOST_USER,
                 [myuser.email]
             )
            email.fail_silently = True
            email.send()

            return redirect('login')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'personne/inscription.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard1"))
        else:
            return redirect("adminDashboard2")
    if request.POST:
        print("1111111111")
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print("1111111111")
            print(email)
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.user_type == '1':
                    return redirect(reverse("adminDashboard1"))
                else:
                     return redirect("adminDashboard2")
        else:
            print("formulaire valide")
            messages.error(request,
                           "votre mot de passe ou votre email est incorrect")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    # print(form)
    return render(request, "personne/connection.html", context)

def VerificationView(self, request, uidb64, token):
        print(89343453)
        return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = Account.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect('login')
    else:
        return render(request, 'personne/Activation_echoue.html')


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user
    profile = Profile.objects.get(user__id=user)
    BASE_WIDTH = 400

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'edit-profile.html', context)

