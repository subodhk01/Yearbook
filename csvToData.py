import django
import csv
import re

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yearbook.settings')

django.setup()
from myapp.models import *
#from myapp import Config as config
from random import *
from django.contrib.auth.models import User


#pswd = config.pswd
ind = 0

with open("form_new_mtech.csv", "rU") as file:
    reader = csv.reader(file, delimiter=',')
    for col in reader:
        ind = ind+1
        email = col[1].strip().lower()
        email = re.sub("iitbhu","itbhu", email )
        username = email[0:-12]
        try:
            dep = str(re.search(r"(?<=\.)(.*)(?=\@)", email).group(0))[-5:-2]
        except:
            print("faulty email")
            continue
        print(username, email)
        s = Student(name=col[0], department= dep, email=email)
        
        try:
            user, created = User.objects.get_or_create(username=username, first_name=col[0], email=email)
            #print(user.email)
            user.save()
            user.student = s
            user.student.save()
            print("success ",ind)
        except:
            print("EXCEPTION: User Already Exists. Continuing")