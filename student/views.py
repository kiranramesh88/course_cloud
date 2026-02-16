from django.shortcuts import render,redirect
from django.views import View
from student.forms import *
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from instructor.models import *
from student.models import *
from django.contrib.auth import authenticate,login
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
import razorpay
from django.http import HttpResponse# Create your views here.
from decouple import config

RAZR_KEY_ID=config('RAZR_KEY_ID')
RAZR_SECRET_KEY=config('RAZR_SECRET_KEY')

class StudentSignupView(View):
    def get(self,request):
        form=StudentCreationForm()
        return render(request,"std_signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form_data=StudentCreationForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login')
        return render(request,"std_signup.html",{"form":form_data})
    
class LandingView(View):
    def get(self,request):
        return render(request,"landing.html")

class StudentLoginView(View):
    def get(self,request):
        form=StudentLoginForm()
        return render(request,"std_login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form_data=StudentLoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request, user)
                if user.role=="Student":
                    return redirect('home')
                elif user.role=="Instructor":
                    return redirect(reverse("admin:index"))
            else :
                return redirect('login')
        return render(request,"std_login.html",{"form":form_data})
    
class HomeView(ListView):
   def get(self,request):
       allcourse_qs=Course.objects.all()
       order_qs=Order.objects.filter(student=request.user,is_paid=True).values_list("course_object",flat=True)
       print(order_qs)
       return render(request,"home.html",{"course":allcourse_qs,"purchased_courses":order_qs})

# class CourseDetailsView(View):
#     def get(self,request,*args,**kwargs):
#         cid=kwargs.get('pk')
#         course=Course.objects.get(id=cid)
#         return render(request,"course_details.html",{"object":course})

class CourseDetailView(DetailView):
    template_name="course_details.html"
    queryset=Course.objects.all()
    context_object_name="object"

class AddtoCartView(View):
    def get(self, request, **kwargs):
        cid = kwargs.get('pk')
        course = Course.objects.get(id=cid)
        user = request.user

        cart_item, created = Cart.objects.get_or_create(
            course_object=course,
            user_object=user
        )

        if created:
            # newly added → go to cart
            return redirect('cart')
        else:
            # already exists → stay on course page
            messages.info(request, "Already added to cart")
            return redirect('course', pk=cid)
        
class CartView(View):
    def get(self,request):
        ptotal=0
        qs=Cart.objects.filter(user_object=request.user)
        for i in qs:
            ptotal+=i.course_object.price
        return render(request,"cart.html",{"data":qs,"ptotal":ptotal})
    

class RemoveFromCartView(View):
    def get(self,request,**kwargs):
        cart_id=kwargs.get('pk')
        Cart.objects.get(id=cart_id).delete()
        return redirect('cart')
    
class PlaceOrderView(View):
    def get(self,request):
        qs=Cart.objects.filter(user_object=request.user)
        student=request.user
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        order=Order.objects.create(student=student,total=cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()
        if cart_total>0:
            client = razorpay.Client(auth=(RAZR_KEY_ID,RAZR_SECRET_KEY))
            data = { "amount": int(cart_total*100), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            print(payment,"++++++++++++")
            order.razr_pay_order_id=payment.get('id')
            order.save()
            context={
                "razr_key_id":RAZR_KEY_ID,
                "amount":int(cart_total*100),
                "display_amount":cart_total,
                "razr_pay_id":payment.get('id')
            }
            print(cart_total)
            return render(request,"payment.html",{"data":context})
        return redirect('home')
    
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerifyView(View):

    def post(self, request):
        print(request.POST)
        client=razorpay.Client(auth=(RAZR_KEY_ID,RAZR_SECRET_KEY))   # check Razorpay response
        try:
            client.utility.verify_payment_signature(request.POST)
            razr_pay_order_id=request.POST.get('razorpay_order_id')
            order_instance=Order.objects.get(razr_pay_order_id=razr_pay_order_id)
            order_instance.is_paid=True
            order_instance.save()
        except:
            print("failed")
        return render(request,"successfull.html")
    
class MyCourseView(View):
    def get(self,request):
        qs=Order.objects.filter(student=request.user,is_paid=True)
        return render(request,"my_courses.html",{"course":qs})

class ViewLessonview(View):
    def get(self,request,**kwargs):
        course=Course.objects.get(id=kwargs.get('pk'))
        query_params=request.GET
        module_id=query_params.get('module') if 'module' in query_params else Module.objects.filter(course=course).first().id
        module_object=Module.objects.get(id=module_id,course=course)
        lesson_id=query_params.get('lesson') if 'lesson' in query_params else Lesson.objects.filter(module_object=module_object).first().id
        lesson=Lesson.objects.get(id=lesson_id,module_object=module_object)
        print(module_id,"******")     
        print(lesson_id,"******")            
        return render(request,"viewLesson.html",{"course":course,"lesson":lesson})
    


    



        