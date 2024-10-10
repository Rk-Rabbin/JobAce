from django.urls import path, include
from . import views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.LandingPage, name='LandingPage'),
    path('home/', views.Home , name='home'),
    path('profile/', views.ProfilePage , name='profile'),
    path('registration/',views.RegistrationView.as_view(), name='registration'),
    path('services/', views.Services , name='services'),
    path('contactus/', views.ContactUs.as_view() , name='contactus'),
    path('chatbot/',views.chatbot_view, name='chatbot'), 
    path('cv_list/',views.CvList, name='cvlist'), 
    path('indiv_cv/<int:id>', views.IndivCv , name='indivcv'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path('favicon.ico', views.favicon_view, name='favicon'),



    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth_app/login.html', authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='auth_app/changepassword.html',
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='auth_app/passwordchangedone.html'),name='passwordchangedone'),

    path('logout/', views.logout_view, name='logout'),



    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='auth_app/password_reset.html', form_class=MyPasswordResetForm),
    name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='auth_app/password_reset_done.html'),
    name='password_reset_done'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='auth_app/password_reset_complete.html'),
    name='password_reset_complete'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth_app/password_reset_confirm.html',
    form_class=MySetPasswordForm), name='password_reset_confirm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
