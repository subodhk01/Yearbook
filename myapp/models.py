# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
	return '{0}/{1}'.format(instance.department, filename)
# Create your models here.
class GenQuestion(models.Model):
	question = models.CharField(max_length=200)
	def __str__(self):
		return self.question

class Poll(models.Model):
	departments = [
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
		("bme", "biotechnology"),
		("bme-idd", "biotechnology IDD"),
		("all", "all")
	]
	poll = models.CharField(max_length=200)
	department = models.CharField(max_length=200,choices=departments)
	votes = JSONField(blank=True,default=dict)
	def __str__(self):
		return self.poll

class Student(models.Model):
	departments = [
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
		("bme", "biotechnology"),
		("bme-idd", "biotechnology IDD"),
		("all", "all")
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100,blank=True)
	department = models.CharField(max_length=100,choices=departments)
	DP = models.ImageField(upload_to="DP",blank=True,default="DP/anonymous.jpg")
	genPic1 = models.ImageField(upload_to=user_directory_path,blank=True)
	genPic2 = models.ImageField(upload_to=user_directory_path,blank=True)
	phone = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=100,blank=True)
	oneliner = models.CharField(max_length=100,blank=True)
	future = models.CharField(max_length=100,blank=True)
	AnswersAboutMyself = JSONField(blank=True,default=dict)
	VotesIHaveGiven = JSONField(blank=True,default=dict)
	CommentsIWrite = JSONField(blank=True,default=list)
	CommentsIGet = JSONField(blank=True,default=list)
	def __str__(self):
		return self.name 




