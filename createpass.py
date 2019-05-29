import random
import csv
import string
def randomString(stringLength=4):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(stringLength))

s=""
with open("pass.csv", "rU") as file:
	reader = csv.reader(file, delimiter=',')
	for col in reader:
		s+=col[0]+","+col[1]+","+col[2]+","+col[3]+","+col[0]+randomString()+"\n"

f=open("pass.csv",'w')
f.write(s)

