#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import time
import json
import urllib3



def getCodigoUnidad(p_unidadDeMedida):
#funcion que devuelve el id al que debemos asignar los datos recuperados	
	v_id = 0
	if(p_unidadDeMedida == 'SO2'):
		v_id = 1
	elif(p_unidadDeMedida == 'CO'):
		v_id = 6
	elif(p_unidadDeMedida == 'NO'):
		v_id = 7
	elif(p_unidadDeMedida == 'NO2'):
		v_id = 8
	elif(p_unidadDeMedida == 'PM2_5'):
		v_id = 9
	elif(p_unidadDeMedida == 'PM10'):
		v_id = 10
	elif(p_unidadDeMedida == 'O3'):
		v_id = 14
	return v_id

# Uno los dataframes para facilitar el tratamiento de la informacion
df1 = pd.read_csv('http://www.mambiente.madrid.es/opendata/horario.txt', delimiter=',', error_bad_lines=False, encoding='latin-1', header=None, names= ['PROVINCIA','MUNICIPIO','ESTACION','MAGNITUD','TÉCNICA','PERIODO ANÁLISIS','AÑO','MES','DIA','H01','V01','H02','V02','H03','V03','H04','V04','H05','V05','H06','V06','H07','V07','H08','V08','H09','V09','H10','V10','H11','V11','H12','V12','H13','V13','H14','V14','H15','V15','H16','V16','H17','V17','H18','V18','H19','V19','H20','V20','H21','V21','H22','V22','H23','V23','H24','V24'])
df2 = pd.read_csv('https://datos.madrid.es/egob/catalogo/212629-1-estaciones-control-aire.csv', delimiter=';',error_bad_lines=False,encoding='latin-1')
df2 = pd.merge(df1, df2, left_on='ESTACION', right_on='CODIGO_CORTO')
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
		del df2['H'+ x + str(i)]
		del df2['V'+ x + str(i)]
	i = i+1

''' 
Estructura para el post con la ultima lectura

{
  "phenomenonTime": "2017-02-07T18:02:00.000Z",
  "resultTime" : "2017-02-07T18:02:05.000Z",
  "result" : 21.6,
  "Datastream":{"@iot.id":8}
}

'''
http = urllib3.PoolManager()
r = http.request('GET','http://63.33.136.20:8080//FROST-Server/v1.0/Things?$expand=Locations&$expand=Datastreams')
data = json.loads(r.data.decode('latin-1'))
dataItems = len(data['value'])
resp = json.dumps(data,indent=4)
y = json.loads(resp)

print(resp.0.value)
#http://localhost:8080/FROST-Server/v1.0/Things?$expand=Datastreams($select=@iot.id,name)




# en y tengo el json con información necesaria de las mediciones
# recorro df2 que tiene el resto de los datos de las mediciones


