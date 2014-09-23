#-*- coding: utf-8 -*-

from datetime import timedelta, date, datetime
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
dict_onibus = dict()

while True:
	fLog = open(loghtml, "a")	
	try:

		path = 'C:\inetpub\wwwroot\onibus'
		listing = os.listdir(path)

		for infile in listing:
			if infile == "template.txt":
				continue
			if "txt" in infile:
				os.remove(path + "\\" + infile)
				continue
		print "Iniciando Request"
		fLog.write("Iniciando Request<br>")
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		document = response.read()
		print "Request finalizado"
		fLog.write("Request Finalizado<br>")
		lines = document.split('\n')
	
		first = True

		onibus = set()
		print "Lendo os dados"
		fLog.write("Lendo os dados<br>")		
		for line in lines:
			if first == True:
				first = False
				continue
			attr = line.split(',')
			dataEHora = getElementInPos(0,attr)
			data = getElementInPos(0,dataEHora.split())
			hora = getElementInPos(1,dataEHora.split())
			month = getElementInPos(0,data.split('-'))
			day = getElementInPos(1,data.split('-'))
			year = getElementInPos(2,data.split('-'))
			hour = getElementInPos(0,hora.split(':'))
			minuto = getElementInPos(1,hora.split(':'))
			segundo = getElementInPos(2,hora.split(':'))	
			if line != '':
				data = datetime(int(year),int(month),int(day), int(hour), int(minuto), int(segundo), 0)
				now = datetime.now()
				if (now - data) > timedelta(minutes=20):
					continue
			else:
				continue
			ordem = getElementInPos(1,attr)
			linha = getElementInPos(2,attr)
			latitude = getElementInPos(3,attr)
			longitude = getElementInPos(4,attr)
			if linha != '':
				if ordem in dict_onibus == True:
					properties = dict_onibus[ordem]
				else:
					properties = []
					properties.append()
					properties.append()
					properties.append("Sentido indefinido")
					dict_onibus[ordem] = properties
				new_properties = []
				new_properties.append(latitude[1:len(latitude)-1])
				new_properties.append(longitude[1:len(longitude)-1])
				pontoFinalFile = "C:\\inetpub\\wwwroot\\onibus\\PontosFinais\\" + linha + ".txt"
				pontoFinal = open(pontoFinalFile, "r")
				pontosFinais = pontoFinal.read().split("\n")
				bairros = [pontosFinais[0].split("\t")[0], pontosFinais[1].split("\t")[0]]
				lats = [pontosFinais[0].split("\t")[1], pontosFinais[1].split("\t")[1]]
				longs = [pontosFinais[0].split("\t")[2], pontosFinais[1].split("\t")[2]]								
				if calc_dist(new_properties[0], new_properties[1], lats[0], longs[0]) <= 500 :
					new_properties.append(bairros[1])
				else if calc_dist(new_properties[0], new_properties[1], lats[1], longs[1]) <= 500 :
					new_properties.append(bairros[0])
				else:
					new_properties.append(properties[2])
				str = "C:\\inetpub\\wwwroot\\onibus\\" + linha + ".txt"
				if linha in onibus:
					fout = open(str, "a")
				else:
					fout = open(str, "w")
					onibus.add(linha)
				fout.write(new_properties[0] + '\t' + new_properties[1] + '\t' + ordem + '\t' + new_properties[2] + '\n')
				fout.close()
		dataPrint = datetime.now()
		print dataPrint
		fLog.write(repr(dataPrint) + "<br>")
	except:
		print "Um erro ocorreu"
		fLog.write("Um erro ocorrer")
		traceback.print_exc(file=sys.stdout)	
		time.sleep(120)
	time.sleep(60)
