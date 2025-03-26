from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from ..decorators import student_required
from ..forms import StdLeaveAppForm,StudentSignUpForm
from ..models import Teacher,Student, User , TeachLeaveApp, StudentLeaveApp
import qrcode
from django.conf import settings
from django.http import HttpResponse
import os
from io import BytesIO



class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students')

def StLeaveApp(request):

    form = StdLeaveAppForm(request.POST)
    
    student = Student.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user=student
        form.save()

    context = {'form':form}

    return render(request,'stApp.html',context)

def StatusOfApp(request):

    student = Student.objects.filter(user=request.user).first()

    app = StudentLeaveApp.objects.filter(user=student).all()

    context = { 'app':app }

    return render(request,'AppStatus.html',context)


def Stpage(request):

    student = Student.objects.filter(user=request.user).first()

    app = StudentLeaveApp.objects.filter(user=student).all()

    context = { 'app':app }

    return render(request,'stpage.html',context)


def leave_application(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, request.FILES)

        # Handle scanned image if present
        scanned_image_data = request.POST.get('scannedImage', None)
        if scanned_image_data:
            # Convert base64 data to an image file
            format, imgstr = scanned_image_data.split(';base64,') 
            ext = format.split('/')[1]  # Extract file extension
            img_data = base64.b64decode(imgstr)  # Decode the base64 string
            image = Image.open(BytesIO(img_data))  # Create an image object
            image_file = ContentFile(img_data, name="scanned_image." + ext)  # Save it as a ContentFile

            # Create a LeaveApplication object and save the image to it
            leave_application = form.save(commit=False)  # Don't save yet, we need to assign the image
            leave_application.supporting_document = image_file  # Set the image field
            leave_application.save()  # Save the LeaveApplication instance with the image

            return redirect('success')  # Redirect to a success page after saving

        if form.is_valid():
            form.save()  # Save the rest of the form data
            return redirect('success')

    else:
        form = LeaveApplicationForm()

    return render(request, 'leave_application_form.html', {'form': form})

def generate_leave_qr(request):
    # Construct a URL to the leave form (you can encode form data, or a link here)
    leave_form_url = "http://example.com/hostel-leave-form/"
    
    # Create QR code from the URL
    qr = qrcode.make(leave_form_url)
    
    # Save the QR code to a memory buffer
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    
    # Set the appropriate content type for the image
    return HttpResponse(buffer, content_type="image/png")