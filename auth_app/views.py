from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, CVUploadForm, UploadForm
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.conf import settings
from .models import User, CV_Model, UploadedCV
from openai import OpenAI
from django.http import JsonResponse
from PyPDF2 import PdfReader
from django.forms import ModelForm
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import sys
import logging

def favicon_view(request):
    return HttpResponse(status=204)  # No content




client = OpenAI(api_key=settings.OPENAI_API_KEY)



# Create your views here.
def LandingPage(request):
    return render(request, 'auth_app/LandingPage.html')

def Services(request):
    return render(request, 'auth_app/services.html')

class ContactUs(View):
    def get(self,request):
        return render(request, 'auth_app/contactus.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')

        email = EmailMessage(
            subject = f"{name} from JobAce",
            body = msg,
            from_email = settings.EMAIL_HOST_USER,
            to = [settings.EMAIL_HOST_USER],
            reply_to = [email]
        )
        email.send()
        messages.success(request, 'Your Feedback Submitted Successfully')
        return render(request, 'auth_app/contactus.html',{'message':messages})

class RegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'auth_app/register.html' , {'form':form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Congratulations!! Successfully Registered')
            except:
                messages.success(request, 'Sorry!! Could not be Registered, Try Again')
        return render(request, 'auth_app/register.html' , {'form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Home(request):
    return render(request, 'auth_app/home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ProfilePage(request):
    usr = request.user
    return render(request, 'auth_app/profile.html',{'usr':usr,'active':'btn-info'})

def logout_view(request):
    logout(request)  # This will log out the user
    return redirect('LandingPage')  # Redirect to the login page or any other success page


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def CvList(request):
    usr = request.user
    try:
        cv = UploadedCV.objects.filter(user=usr)
    except:
        cv = None
    if(cv!=None):
        return render(request, 'auth_app/cv_list.html',{'cv':cv})
    else:
        return render(request, 'auth_app/cv_list.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def IndivCv(request,id):
    try:
        cv = UploadedCV.objects.get(id=id)
    except UploadedCV.DoesNotExist:
        cv = None
    if(cv!=None):
        return render(request, 'auth_app/indiv_cv.html',{'cv':cv})
    else:
        return render(request, 'auth_app/indiv_cv.html',{'cv':cv})


sys.setrecursionlimit(1500)  # Set the recursion limit

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def upload_cv(request):
    form = UploadForm()  # Initialize the form here

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)  # Update form with POST data
        if form.is_valid():
            cv_instance = form.save(commit=False)
            cv_instance.user = request.user
            cv_instance.save()
            messages.success(request, 'Congratulations! Successfully Uploaded')
            return redirect('upload_cv')
        else:
            # Print form errors to console
            print("Form errors:", form.errors)
            messages.error(request, 'There was an error uploading your CV. Please try again.')

    return render(request, 'auth_app/upload.html', {'form': form})





def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ''
            return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""



# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required
# def chatbot(request):
#     usr = request.user
#     chatbot_response = None  # Initialize chatbot_response variable
#     user_input = None  # Initialize user_input variable

#     if request.method == 'POST':
#         user_input = request.POST.get('userMessage')
#         prompt = user_input

#         try:
#             # Make the API request to OpenAI
#             response = openai.Completion.create(
#                 engine='text-davinci-003',
#                 prompt=prompt,
#                 max_tokens=256,
#                 temperature=0.5,
#             )

#             # Check the HTTP status code in the response
#             if response.status_code == 200:
#                 chatbot_response = response.choices[0].text  # Store chatbot response

#         except Exception as e:
#             # Handle any exceptions that may occur during the API request
#             error_message = f"An error occurred: {str(e)}"
#             return render(request, 'mediaid/chat.html', {
#                 'usr': usr,
#                 'error_message': error_message,
#                 'active': 'btn-info'
#             })

#     # Render the chat.html template with chatbot_response and user_input
#     return render(request, 'auth_app/chat.html', {
#         'usr': usr,
#         'response': chatbot_response,
#         'user_input': user_input,
#         'active': 'btn-info'
#     })

logger = logging.getLogger(__name__)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get("userMessage")  # Ensure this matches your frontend

        try:
            # Call the OpenAI Chat API to get a response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Specify the model to use
                messages=[
                    {"role": "user", "content": user_input}  # User input message
                ]
            )
            chatbot_reply = response.choices[0].message.content.strip()  # Get the chatbot's reply

        except Exception as e:
            chatbot_reply = "There was an error with the chatbot service."
            logger.error(f"Error while calling OpenAI API: {e}")  # Log the error for debugging

        return JsonResponse({"response": chatbot_reply})

    # If the request method is not POST, render the chat template
    return render(request, 'auth_app/chat.html', {'active': 'btn-info'})