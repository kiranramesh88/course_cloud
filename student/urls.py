from django.urls import path
from student.views import *

urlpatterns=[
    path('home',HomeView.as_view(),name="home"),
    path('std_signup',StudentSignupView.as_view(),name="std_signup"),
    path('stdlogin',StudentLoginView.as_view(),name="login"),
    path('course/<int:pk>',CourseDetailView.as_view(),name="course"),
    path('addtocart/<int:pk>',AddtoCartView.as_view(),name="addcart"),
    path('cart',CartView.as_view(),name="cart"),
    path('removefromcart/<int:pk>',RemoveFromCartView.as_view(),name="delcart"),
    path('placeorder',PlaceOrderView.as_view(),name="order"),
    path('mycourse',MyCourseView.as_view(),name="mycourse"),
    path('viewlesson/<int:pk>',ViewLessonview.as_view(),name="viewlesson"),
    path('verify/',PaymentVerifyView.as_view(),name="verify")
]