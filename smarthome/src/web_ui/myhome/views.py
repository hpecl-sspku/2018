# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse


from . import models
# Create your views here.

def index(request):
	nodedata = models.Nodedata.objects.order_by('-id')[0]
	commands = models.Commands.objects.get(pk=1)
	return render(request, 'myhome/index.html', {'commands': commands, 'nodedata': nodedata})
#	return render(request, 'myhome/index.html', {'commands': commands, 'nodedata': nodedata.toJSON})

@csrf_exempt
def index_ajax(request):
	print(request.POST)
	if request.method=='POST':
		temp_command =request.POST.get('ac1_command','')
	
	#AC_OPEN\AC_CLOSE  NORMALMODE AUTOMODE  AC_COLD  AC_WARM OPEN_AUDIO CLOSE_AUDIO
	if temp_command == '1':
		obj = models.Commands.objects.filter(id=1).update(intent='AC_OPEN')
	if temp_command == '2':
		obj = models.Commands.objects.filter(id=1).update(intent='AC_CLOSE')
	if temp_command == '3':
		obj = models.Commands.objects.filter(id=1).update(intent='NORMALMODE')
	if temp_command == '4':
		obj = models.Commands.objects.filter(id=1).update(intent='AUTOMODE') 
	if temp_command == '5':
		obj = models.Commands.objects.filter(id=1).update(intent='AC_COLD') 
	if temp_command == '6':
		obj = models.Commands.objects.filter(id=1).update(intent='AC_WARM') 
	if temp_command == '7':
		obj = models.Commands.objects.filter(id=1).update(intent='OPEN_BOX') 
	if temp_command == '8':
		obj = models.Commands.objects.filter(id=1).update(intent='CLOSE_BOX') 
	if temp_command == '9':
		obj = models.Commands.objects.filter(id=1).update(intent='OPEN_PPT') 
	if temp_command == '10':
		obj = models.Commands.objects.filter(id=1).update(intent='CLOSE_PPT') 
	return render(request, 'myhome/index.html') 
	#return HttpResponseRedirect(reverse('index'))
	
	
def bar1(request):
	nodedatas = models.Nodedata.objects.all()
	listx = []
	listy = []
	datetmp = '0'
	flag = 0
	for nodedata in nodedatas[::-1]:
		date = str(nodedata.time)[0:10]
		if datetmp == date:
			pass
		else:
			datetmp = date
			flag = flag + 1
			if flag == 8:
				break
			else:
				listx.append(str(date))
				listy.append(float(nodedata.temperature))
	listx = listx[::-1]
	listy = listy[::-1]
	return render(request, 'myhome/bar1.html', {'nodedatas':nodedatas, 'X':listx, 'Y':listy})

def bar2(request):
	nodedatas = models.Nodedata.objects.all()
	listx = []
	listy = []
	datetmp = '0'
	flag = 0
	for nodedata in nodedatas[::-1]:
		date = str(nodedata.time)[0:10]
		if datetmp == date:
			pass
		else:
			datetmp = date
			flag = flag + 1
			if flag == 8:
				break
			else:
				listx.append(str(date))
				listy.append(float(nodedata.humidity))
	listx = listx[::-1]
	listy = listy[::-1]
	return render(request, 'myhome/bar2.html', {'nodedatas':nodedatas, 'X':listx, 'Y':listy})

def bar3(request):
	nodedatas = models.Nodedata.objects.all()
	listx = []
	listy = []
	datetmp = '0'
	flag = 0
	for nodedata in nodedatas[::-1]:
		date = str(nodedata.time)[0:10]
		if datetmp == date:
			pass
		else:
			datetmp = date
			flag = flag + 1
			if flag == 8:
				break
			else:
				listx.append(str(date))
				listy.append(float(nodedata.light))
	listx = listx[::-1]
	listy = listy[::-1]
	return render(request, 'myhome/bar3.html', {'nodedatas':nodedatas, 'X':listx, 'Y':listy})

def bar4(request):
	nodedatas = models.Nodedata.objects.all()
	listx = []
	listy = []
	datetmp = '0'
	flag = 0
	for nodedata in nodedatas[::-1]:
		date = str(nodedata.time)[0:10]
		if datetmp == date:
			pass
		else:
			datetmp = date
			flag = flag + 1
			if flag == 8:
				break
			else:
				listx.append(str(date))
				listy.append(float(nodedata.co2_simulation))
	listx = listx[::-1]
	listy = listy[::-1]
	return render(request, 'myhome/bar4.html', {'nodedatas':nodedatas, 'X':listx, 'Y':listy})

def bar5(request):
	nodedatas = models.Nodedata.objects.all()
	listx = []
	listy = []
	datetmp = '0'
	flag = 0
	for nodedata in nodedatas[::-1]:
		date = str(nodedata.time)[0:10]
		if datetmp == date:
			pass
		else:
			datetmp = date
			flag = flag + 1
			if flag == 8:
				break
			else:
				listx.append(str(date))
				listy.append(float(nodedata.noise))
	listx = listx[::-1]
	listy = listy[::-1]
	return render(request, 'myhome/bar5.html', {'nodedatas':nodedatas, 'X':listx, 'Y':listy})
