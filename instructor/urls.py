from django.urls import path
from instructor.views import *


urlpatterns=[
    path('instructorsignup',InstructorSignUpview.as_view(),name="instructor")
]