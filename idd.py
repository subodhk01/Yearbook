import django
import csv
import re

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yearbook.settings')

django.setup()
from myapp.models import *
from django.contrib.auth.models import User
from django.db.models import F

#students = Student.objects.filter(email__contains="15@").update(department=("%s-idd" % (F('department'),)) )
students = Student.objects.filter(email__contains="15@")
for s in students:
    s.department = str(s.department) + "-idd"
    print(s.department)
    s.save()

