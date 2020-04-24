import django
import csv
####
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yearbook.settings')
####
django.setup()
from myapp.models import *

poll_filename  = "./Scrape/polls.csv"

depts = [
		("che", "chemical"),
		("che-idd", "chemical IDD"),
		("cer", "ceramic"),
		("cer-idd", "ceramic IDD"),
		("civ", "civil"),
		("civ-idd", "civil IDD"),
		("cse", "computer science"),
		("cse-idd", "computer science IDD"),
		("eee", "electrical"),
		("eee-idd", "electrical IDD"),
		("ece", "electronics"),
		("mat", "mathematics"),
		("mat-idd", "mathematics IDD"),
		("mec", "mechanical"),
		("mec-idd", "mechanical IDD"),
		("min", "mining"),
		("min-idd", "mining IDD"),
		("phe", "pharma"),
		("phe-idd", "pharma IDD"),
		("chy", "chemistry"),
		("chy-idd", "chemistry IDD"),
		("met", "metallurgy"),
		("met-idd", "metallurgy IDD"),
		("mst", "material"),
		("mst-idd", "material IDD"),
		("hss", "humanities"),
		("phy", "physics"),
		("phy-idd", "physics IDD"),
		("bce", "biotechnology"),
		("bce-idd", "biotechnology IDD"),
		("bme", "biomedical"),
		("bme-idd", "biomedical IDD"),
	]

def addPoll(poll_quest,dept):
    u = Poll(poll=poll_quest, department=dept)
    u.save()
    print(poll_quest,"------>",dept)
                
    return

with open(poll_filename, "rU") as file:
    reader = csv.reader(file, delimiter=',')
    for col in reader:
        poll_quest = col[1]
        if(col[0]=="all"):
            for dept in depts:
                addPoll(poll_quest,dept[0])
        elif col[0]=="com":
            addPoll(poll_quest,"all")
        elif(col[0]=="var"):
            for dept in depts:
                poll_quest_dept = poll_quest.replace("$DEPT$",dept[1])
                addPoll(poll_quest_dept,dept[0])
        elif(col[0][0]=="!"):
            for dept in depts:
                if(dept[0]!=col[0][1:]):
                    addPoll(poll_quest,dept[0])
        else:
            for dept in depts:
                if(dept[0]==col[0]):
                    addPoll(poll_quest,dept[0])
