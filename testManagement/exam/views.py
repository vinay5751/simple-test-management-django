from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from . models import Student,Teacher,StudentProfile,TeacherProfile,Test
from django.core.files.storage import FileSystemStorage
from . forms import TestForm

# Create your views here.
def index(request):
    return render(request, "index.html")

def signupUser(request):
    return render(request,"signup.html")

def studentSignup(request):
    return render(request,"signupStudent.html")

def teacherSignup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        subject = request.POST.get("subject")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Teacher.objects.create_user(fname=fname,lname=lname,email=email,password=password)
        TeacherProfile.objects.create(user=user,subject=subject)
        return HttpResponse("<h1>Teacher Account Created</h1>")

    return render(request,"signupTeacher.html")

def studentSignup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        standard = request.POST.get("standard")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Student.objects.create_user(fname=fname,lname=lname,email=email,password=password)
        StudentProfile.objects.create(user=user,standard=standard)
        return HttpResponse("<h1>Student Account Created</h1>")

    return render(request,"signupStudent.html") 

def studentview(request):
    tests = Test.objects.all()
    return render(request,"studentView.html",{"tests":tests})

def teacherview(request):
    form = TestForm()
    tests = Test.objects.all() 
    return render(request,"teacherView.html",{"form":form,"tests":tests})

def loginUser(request):
    if request.method == 'POST':
        accountType = request.POST.get("account-type")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if (user is not None) :
            if user.is_student and accountType == "student":
                login(request, user)
                return studentview(request)
            elif user.is_teacher and accountType == "teacher":
                login(request, user)
                return teacherview(request)
    
    return render(request,"index.html")

def logoutUser(request):
    logout(request)
    return render(request,"index.html")


def uploadtest(request):
    if request.method == "POST":
        form = TestForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            tests = Test.objects.all() 
            return render(request,"teacherView.html",{"form":form,"tests":tests})
    else:
        form = TestForm()    

    return render(request , "teacherView.html",{"form":form})

def delete(request, id):
    obj = Test.objects.get(id=id)
    obj.delete()
    form = TestForm()
    tests = Test.objects.all() 
    return render(request,"teacherView.html",{"form":form,"tests":tests})

    