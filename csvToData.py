import django
import csv
import re



django.setup()
from myapp.models import *
#from myapp import Config as config
from random import *
from django.contrib.auth.models import User


#pswd = config.pswd
ind = 0

with open("form_new.csv", "rU") as file:
    reader = csv.reader(file, delimiter=',')
    for col in reader:
        ind = ind+1
        user_passwd = col[2].strip()
        username = re.search(r"([^@]+)", col[1].strip()).group(0).lower()
        email = col[1].strip()
        email = re.sub("iitbhu","itbhu", email )
        try:
            dep = str(re.search(r"(?<=\.)(.*)(?=\@)", email).group(0))[-5:-2]
        except:
            print("faulty email")
            continue
        print(username, email, user_passwd)
        #u = User.objects.create_user(username=username, password=user_passwd ,email=email)
        #u.save()
        s = Student(name=col[0], department= dep)
        #u.student = s
        #u.student.save()
        #u = User(username=username, password=user_passwd, email=email)
        
        try:
            user, created = User.objects.get_or_create(username=username)
            user.set_password(user_passwd)
            user.email = email
            print(user.email)
            user.save()
            user.student = s
            user.student.save()
            print("success ",ind)
        except:
            print("EXCEPTION: User Already Exists. Continuing")