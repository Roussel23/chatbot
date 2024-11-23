
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import django

from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import  force_bytes ,force_str, DjangoUnicodeDecodeError
import django.utils

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from .models import Chat
from django.utils import regex_helper

import openai
# from openai import OpenAI


from django.utils import timezone
from random import randint




from django.contrib.auth.decorators import login_required




import datetime
from django.utils.timezone import now

import google.generativeai as genai
import os


# Create your views here.

def validate_email(self,email):
    if(len(email)<7):
        return False
    else:
        regex_helper.contains(email)
        return True
    



class EmailValidationView(View):
    def post(self, request):
        #recupere la donnée saisi par l'utilisateur
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email est invalide'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'desolé l\'email est utilisé,choississez un autre '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Le nom d\'utilisateur doit seulement contenir des caracteres alphanumeriques'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'desole le nom d\'utilisateur est utilisé , choississez un autre '}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Le mot de passe est trop petit')
                    return render(request, 'signup.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Salut '+user.username + ', S\'il vous plait le lien en dessous permet d\'activé votre compte \n'+activate_url,
                    'chatbot@semycolon.com',
                    [email],
                )
                
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                
                # email.send(fail_silently=False)
                messages.success(request, 'Le compte a été crée avec succès')
                return render(request, 'chat.html')

        return redirect('signup.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'Utilisateur existe deja')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Le compte a été activé avec succès')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Bienvenue, ' +
                                     user.username+' vous êtes maintenant connecté ')
                    return redirect('chat')
                messages.error(
                    request, 'Le compte n\'est pas active, S\'il vous plait verifiez votre email')
                return render(request, 'login.html')
            messages.error(
                request, 'Cet utilisateur n\'existe pas, essayez encore...')
            return render(request, 'login.html')

        messages.error(
            request, 'S\'il vous plait remplissez tous les champs')
        return render(request, 'login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Vous êtes maintenant deconnecter')
        return redirect('login')


# openai_api_key = 'api_key'
# openai.api_key = openai_api_key
# setx OPENAI_API_KEY "your_api_key_here"
# gpt-4o-mini
# def ask_openai(message):
#     response = openai.ChatCompletion.create(  
#         # model = "gpt-4",
#         # messages=[
#         #     {"role": "system", "content": "You are an helpful assistant."},
#         #     {"role": "user", "content": message},
#         # ]
#         engine="text-davinci-003",
#         prompt=message,
#         max_tokens=150
#     )
    
#     # answer = response.choices[0].message.content.strip()
    
#     answer = response.choices[0].text.strip()
#     return answer



def askgemini(message):
    genai.configure(api_key="enter_your_api_key")
    

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[]
    )

    response = chat_session.send_message(message)
    return response.text


@login_required(login_url='/login')
def chat(request):
    chats=[]
    chats = Chat.objects.filter(username = request.user.username)
    
    
 
    if request.method == 'GET':
        return render(request, 'chat.html', {'chats': chats})
    if request.method == 'POST':
        message = request.POST.get('input_chat')
        if message:
           
            response = askgemini(message)           
            
            
            idM= randint(0,20000)
            chat = Chat(id = idM,username = request.user.username, question = message, response = response , date=timezone.now())
            chat.save()
            message=""
           
            return render(request, 'chat.html', {'chats': chats})
           
        else:
            messages.success(request, 'Le champ ne peut etre vide')
            message=""
        message=""
    return render(request, 'chat.html', {'chats': chats})


@login_required(login_url='/login')   
def history(request):
    chats=[]
    chats = Chat.objects.filter(username =request.user.username)

    return render(request, 'history.html',  {'chats': chats})