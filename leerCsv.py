#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
from pandas.io.json import json_normalize
import time
import json
import urllib3

def getCodigoUnidad(p_unidadDeMedida):
#funcion que devuelve el id al que debemos asignar los datos recuperados	
	v_id = ''
	if(p_unidadDeMedida == 1):
		v_id = 'SO2'
	elif(p_unidadDeMedida == 6):
		v_id = 'CO'
	elif(p_unidadDeMedida == 7):
		v_id = 'NO'
	elif(p_unidadDeMedida ==  8):
		v_id = 'NO2'
	elif(p_unidadDeMedida == 9):
		v_id = 'PM2_5'
	elif(p_unidadDeMedida == 10):
		v_id = 'PM10'
	elif(p_unidadDeMedida == 14):
		v_id = 'O3'
	return v_id

def getIotId(p_est, p_mag):
	codigo = p_mag + ' - ' + str(p_est)
	headers = {'Content-Type': 'application/json'}	
	response = requests.get('http://localhost:8080/FROST-Server/v1.0/Things?$filter=name%20eq%20' + str(p_est) +'&$select=@iot.id', headers=headers)	
	response_native = json.loads(response.text)
	k = response_native['value'][0]
	iotIdThing = list(k.items())[0][1]	
	response = requests.get("http://localhost:8080/FROST-Server/v1.0/Things("+ str(iotIdThing) + ")/Datastreams?$select=@iot.id&$filter=name eq '" + codigo +  "'", headers=headers)
	response_native = json.loads(response.text)		
	try:
		k = response_native['value']
		iotIdDatastream = list(k[0].items())[0][1]		
		return str(iotIdDatastream)
	except (IndexError, ValueError):
		return ''

# Uno los dataframes para facilitar el tratamiento de la informacion
df1 = pd.read_csv('http://www.mambiente.madrid.es/opendata/horario.txt', delimiter=',', error_bad_lines=False, encoding='latin-1', header=None, names= ['PROVINCIA','MUNICIPIO','ESTACION','MAGNITUD','TECNICA','PERIODO ANALISIS','ANIO','MES','DIA','H01','V01','H02','V02','H03','V03','H04','V04','H05','V05','H06','V06','H07','V07','H08','V08','H09','V09','H10','V10','H11','V11','H12','V12','H13','V13','H14','V14','H15','V15','H16','V16','H17','V17','H18','V18','H19','V19','H20','V20','H21','V21','H22','V22','H23','V23','H24','V24'])

# Selecciono la hora que se va a introducir en el servidor Frost
hora = time.localtime().tm_hour+2 #se incrementa en 2 la hora para ajustar la hora del sistema a la real de Madrid
if(hora < 10):
	if(hora == 0):
		horaConsultada = 'H24'
		consultaValida = 'V24'	
	else:
		horaConsultada = 'H0'+str(hora)
		consultaValida = 'V0'+str(hora)
else:
	if(hora > 24):
		hora = hora - 24
		horaConsultada = 'H0'+str(hora)
		consultaValida = 'V0'+str(hora) 
	else:
		horaConsultada = 'H'+str(hora)
		consultaValida = 'V'+str(hora)
i=1
while i < 25:
	x = ''
	if i < 10:
		x = '0'
	if (horaConsultada != 'H'+ x + str(i)):		
		del df1['H'+ x + str(i)]
		del df1['V'+ x + str(i)]
	i = i+1

export_csv = df1.to_csv(r'./openDatas/datos.csv', index = None, header= True)

# Iteración por filas del DataFrame:
h = str(horaConsultada)
for indice_fila, fila in df1.iterrows():
	uni = getCodigoUnidad(fila["MAGNITUD"])	
	if(uni != ''):		
		iotId = getIotId(fila["ESTACION"],getCodigoUnidad(fila["MAGNITUD"]))			
		if(iotId != ''):
			resultado = '{"phenomenonTime": "'+ str(fila["ANIO"]) + '-' + str(fila["MES"]) + '-' + str(fila["DIA"]) + 'T'+ str(hora)+':00:00.000Z","resultTime": "'+ str(fila["ANIO"]) + '-' + str(fila["MES"]) + '-' + str(fila["DIA"]) + 'T'+ str(hora)+':00:00.000Z","result":'+str(fila[h])+',"Datastream":{"@iot.id":' + str(iotId) +'}}'	
			print(resultado)
			if(fila[h] != 0):
				print(resultado)		
				headers = {'Content-Type': 'application/json'}				
				response = requests.post('http://localhost:8080/FROST-Server/v1.0/Observations', headers=headers, data=resultado)	
				print(iotId) 
				print(response)
	
