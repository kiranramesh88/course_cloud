from django.shortcuts import render,redirect
from django.views import View
from instructor.forms import *
from django.contrib import messages

 
# Create your views here.

class InstructorSignUpview(View):
    def get(self,request,*args,**kwargs):
        form=InstructorForm()
        return render(request,"instr_signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form_data=InstructorForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"Instructor Signup Successfull")
            return redirect('instructor')
        return render(request,"instr_signup.html",{"form":form_data})