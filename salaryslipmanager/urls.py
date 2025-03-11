from django.urls import path
from .views import *

urlpatterns = [
    path('', salary_slip_form),
    path('file/', generate_salary_slip_pdf)
]
