from django.shortcuts import render, redirect
from django.contrib import messages 
from userauths import forms as userauths_forms
from django.contrib.auth import authenticate, login, logout
from doctor import models as doctor_models
from patient import models as patient_models


def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are logged in already")
        return redirect("/")
    
    form = userauths_forms.UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        full_name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        user_type = form.cleaned_data.get("user_type")

        user = authenticate(request, email=email, password=password1)
        print("user type ========= ", user)
        
        if user is not None:
            login(request, user)
    
        
        if user_type == "Doctor":
            doctor_models.Doctor.objects.create(user=user, full_name=full_name)
        else:
            patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)


        messages.success(request, "Account created successfully")
        return redirect("/")
    
    else:
        messages.error(request, "Authentication failed, please try again later!")

    context = {
        "form":form
    }
    return render(request, "userauths/sign-up.html", context)
