import django
import csv
django.setup()
from myapp.models import *
#from myapp import Config as config
from random import *
from django.contrib.auth.models import User


#pswd = config.pswd
ind = 0

with open("pass.csv", "rU") as file:
	reader = csv.reader(file, delimiter=',')
	for col in reader:	
		ind = ind+1
		pswd = col[0]
		randomnumber=""+str(randint(10, 99))
		user_passwd = col[4].strip()
		u = User(username=col[0].lower(), password=user_passwd)
		s = Student(name=col[1], department=col[2])
		print(col[0]+","+col[1]+","+col[2]+","+user_passwd)
		try:
			user, created = User.objects.get_or_create(username=col[0].lower)
			user.set_password(user_passwd)
			user.save()
			user.student = s
			user.student.save()
		except:
			print("EXCEPTION: User Already Exists. Continuing")
