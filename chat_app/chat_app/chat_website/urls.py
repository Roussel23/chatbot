from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    
    # path('login/', views.login, name="login"),
    # path('register/', views.register, name="register"),
    # path('chat/', views.chat, name="chat"),
    # path('view_chat/', views.view_chat, name="view_chat"),
    # path('history/', views.chat, name="history"),

    
    
    path('register', views.RegistrationView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         views.VerificationView.as_view(), name='activate'),
    
    path('', views.chat, name="chat"),
    path('send/', views.chat, name="chat"),
    path('history/', views.history, name="history"),
    path('<str:pk>',views.chat,name="show")
#     path('send_chat', views.send_chat, name="send_chat"),
     
    
]
