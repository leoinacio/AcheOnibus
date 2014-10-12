#-*- coding: utf-8 -*-

from datetime import timedelta, date, datetime
from operator import itemgetter, attrgetter
import urllib,urllib2
import time
import os
import sys, traceback
import math
from array import *

def calc_dist(lat1, long1, lat2, long2):
	lat1Radians = math.radians(90-lat1)
	lat2Radians = math.radians(90-lat2)
	longRadians = math.radians(long1-long2)
	dist = math.acos(math.cos(lat1Radians) * math.cos(lat2Radians) + math.sin(lat1Radians) * math.sin(lat2Radians) * math.cos(longRadians)) * 6371
	return dist * 1000

def getElementInPos(pos, lista):
	i = 0
	dummy = ""
	for item in lista:
		if i == pos:
			return item
		i = i+1
	return dummy

url = "http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm"

loghtml = "C:\\inetpub\\wwwroot\\onibus\\log.htm"
path = 'C:\inetpub\wwwroot\onibus'
dict_onibus = dict()
onibus = set()
toRemove = set()
		
listings = os.listdir(path)
for arquivo in listings:
	if "txt"in arquivo:
		os.remove(path + "\\" + arquivo)
		
while True:
	fLog = open(loghtml, "a")	
	try:

		print ("Iniciando Request")
		fLog.write("Iniciando Request<br>")
		request = urllib2.Request(url)
		print ("...")
		fLog.write("...<br>")
		response = urllib2.urlopen(request, timeout = 60)
		document = response.read()

		print ("Request finalizado")
		fLog.write("Request Finalizado<br>")
		
		lines = document.split('\n')
		first = True

		print ("Lendo os dados")
		fLog.write("Lendo os dados<br>")		
		
		lista_onibus = []
		for line in lines:
			if first == True:
				first = False
				continue
			attr = tuple(line.split(','))
			if len(attr) < 6:
				continue
			lista_onibus.append(attr)
		lista_onibus = sorted(lista_onibus, key=itemgetter(2))   
		previous_line = "blah"
		texto = ""
		for bus_tuple in lista_onibus:
			dataEHora = getElementInPos(0,bus_tuple)
			data = getElementInPos(0,dataEHora.split())
			hora = getElementInPos(1,dataEHora.split())
			month = getElementInPos(0,data.split('-'))
			day = getElementInPos(1,data.split('-'))
			year = getElementInPos(2,data.split('-'))
			hour = getElementInPos(0,hora.split(':'))
			minuto = getElementInPos(1,hora.split(':'))
			segundo = getElementInPos(2,hora.split(':'))	
			data = datetime(int(year),int(month),int(day), int(hour), int(minuto), int(segundo), 0)
			now = datetime.now()
			if (now - data) > timedelta(minutes=20):
				continue
			ordem = getElementInPos(1,bus_tuple)
			linha = getElementInPos(2,bus_tuple)
			latitude = getElementInPos(3,bus_tuple)
			longitude = getElementInPos(4,bus_tuple)
			if linha != '':
				new_properties = []
				new_properties.append(latitude[1:len(latitude)-1])
				new_properties.append(longitude[1:len(longitude)-1])
				new_properties.append("Sentido Indefinido")
				new_properties.append(dataEHora)
				str = "C:\\inetpub\\wwwroot\\onibus\\" + linha + ".txt"
				if linha != previous_line:
					if previous_line != "blah":
						fout.write(texto)
						texto = ""
						fout.close()
					fout = open(str, "w")
					previous_line = linha
					toRemove.add(str)
					onibus.discard(str)
				texto += new_properties[0] + '\t' + new_properties[1] + '\t' + ordem + '\t' + new_properties[2] +'\t' + new_properties[3] + '\n'
		fout.write(texto)
		texto = ""
		fout.close()
		for entry in onibus:
			os.remove(entry)
		onibus = toRemove
		toRemove = set()
		dataPrint = datetime.now()
		print (dataPrint)
		fLog.write(repr(dataPrint) + "<br>")	
	except:
		print ("Um erro ocorreu")
		fLog.write("Um erro ocorrer")
		traceback.print_exc(file=sys.stdout)	
		time.sleep(20)
	time.sleep(40)
