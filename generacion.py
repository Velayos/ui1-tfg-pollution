#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import requests
import pandas as pd
import json
import time

# GENERACION.PY
# AUTOR: JESUS VELAYOS.
# TUTOR: SERGIO TRILLES.
# VERSION: 1.0

# PROGRAMA QUE CREA LOS THINGS, DATASTREAMS, LOCATIONS Y SENSORS
# QUE SON REQUISITOS PREVIOS A LA EJECUCION DEL PROCEDIMIENTO PRINCIPAL DEL TFG
# Se genera un archivo por cada centro de medicion

def f_unidadDeMedida(p_unidadDeMedida):
	#['NO2','SO2','CO','PM10','PM2_5','O3']
	v_texto = ''
	if(p_unidadDeMedida == 'NO2'):
		v_texto = "µg/m3"
	elif(p_unidadDeMedida == 'SO2'):
		v_texto = "µg/m3"
	elif(p_unidadDeMedida == 'CO'):
		v_texto = "mg/m3"
	elif(p_unidadDeMedida == 'PM10'):
		v_texto = 'µg/m3'
	elif(p_unidadDeMedida == 'PM2_5'):
		v_texto = 'µg/m3'
	elif(p_unidadDeMedida == 'O3'):
		v_texto = 'µg/m3'
	return v_texto

def f_definicion(p_unidadDeMedida):
	#['NO2','SO2','CO','PM10','PM2_5','O3']
	v_texto = ''
	if(p_unidadDeMedida == 'NO2'):
		v_texto = "microgramos por metro cúbico"
	elif(p_unidadDeMedida == 'SO2'):
		v_texto = "microgramos por metro cúbico"
	elif(p_unidadDeMedida == 'CO'):
		v_texto = "miligramos por metro cúbico"
	elif(p_unidadDeMedida == 'PM10'):
		v_texto = "microgrammos por metro cúbico"
	elif(p_unidadDeMedida == 'PM2_5'):
		v_texto = "miligramos por metro cúbico"
	elif(p_unidadDeMedida == 'O3'):
		v_texto = "miligramos por metro cúbico"
	return v_texto


def f_incluirDatastream (p_unidad):
	#['NO2','SO2','CO','PM10','PM2_5','O3']
	ds_json = '{'
	ds_json = ds_json + '"name": "' + p_unidad + ' - ' + str(fila["CODIGO_CORTO"]) + '", '
	ds_json = ds_json + '"description": "Concentracion de ' + p_unidad + ' en ' + fila["ESTACION"] + '", '
	ds_json = ds_json + '"observationType": "AmountOfSubtancePerUnitVolume",'
	ds_json = ds_json + '"unitOfMeasurement": {'
	ds_json = ds_json + '"name": "' + f_unidadDeMedida(p_unidad)  + '", '
	ds_json = ds_json + '"symbol": "' + p_unidad + '",'
	ds_json = ds_json + '"definition": "' + f_definicion(p_unidad) + '"}, '
	ds_json = ds_json + '"Sensor": {'
	ds_json = ds_json + '"name": "Sensor de ' + p_unidad + ' - ' + fila["ESTACION"] + '", '
	ds_json = ds_json + '"description": "Medidor de concentracion de ' + p_unidad + '", '
	ds_json = ds_json + '"encodingType": "application/pdf", '
	ds_json = ds_json + '"metadata": "http://www.mambiente.munimadrid.es/opencms/export/sites/default/calaire/Anexos/aparatos_de_medida.pdf"}, '
	ds_json = ds_json + '"ObservedProperty": {'
	ds_json = ds_json + '"name": ' + '"' + p_unidad + '",'
	ds_json = ds_json + '"definition": "http://www.mambiente.munimadrid.es/opencms/export/sites/default/calaire/Anexos/aparatos_de_medida.pdf", '
	ds_json = ds_json + '"description": "Concentracion de ' + p_unidad + '"'
	return ds_json

baseUrl = "https://datos.madrid.es/egob/catalogo/212629-1-estaciones-control-aire.csv"
headers = {'Content-type': 'application/json'}
#unidades = ['NO2','SO2','CO','PM10','PM2_5','O3']

df = pd.read_csv(baseUrl, delimiter=';',error_bad_lines=False,encoding='latin-1');
print('**********************************')
print('Iniciando proceso de carga inicial')
print('**********************************')
datas = ''
for indice_fila, fila in df.iterrows():		
	# things y locations
	if (datas == ''):		
		datas = '{"name": "'  + str(fila["CODIGO_CORTO"]) + '", "description": "' + fila["DIRECCION"] + '", "Locations": [{"name": "' + fila["ESTACION"] + '", "description": "' + str(fila["CODIGO_CORTO"]) + ' - ' + fila["ESTACION"] + '", "encodingType": "application/vnd.geo+json", "location":  { "type": "Point", "coordinates": [' + str(fila["LONGITUD"]) + ', ' + str(fila["LATITUD"]) + ']}}]'
	else:
		datas = datas + ',{"name": "'  + str(fila["CODIGO_CORTO"]) + '", "description": "' + fila["DIRECCION"] + '", "Locations": [{"name": "' + fila["ESTACION"] + '", "description": "' + str(fila["CODIGO_CORTO"]) + ' - ' + fila["ESTACION"] + '", "encodingType": "application/vnd.geo+json", "location":  { "type": "Point", "coordinates": [' + str(fila["LONGITUD"]) + ', ' + str(fila["LATITUD"]) + ']}}]'

	#['NO2','SO2','CO','PM10','PM2_5','O3']
	datas = datas + ', "Datastreams": ['
	if (fila["NO2"] == 'X'):
		datas = datas + f_incluirDatastream("NO2") 
	if (fila["SO2"] == 'X'):
		datas = datas + '}},'+ f_incluirDatastream("SO2") 
	if (fila["CO"]  == 'X'):
		datas = datas  + '}},' + f_incluirDatastream("CO")
	if (fila["PM10"]  == 'X'):
		datas = datas  + '}},' + f_incluirDatastream("PM10")
	if (fila["PM2_5"]  == 'X'):
		datas = datas + '}},' + f_incluirDatastream("PM2_5") 
	if (fila["O3"]  == 'X'):
		datas = datas + '}},' + f_incluirDatastream("O3") 
	datas = datas + '}}]}'
	# se envia el fichero al servidor frost para la inserción
	
	print('generando archivo para ' + str(fila["CODIGO_CORTO"]))
	with open('./json/'+ str(fila["CODIGO_CORTO"]) + '.json', 'w+') as f:		
		f.write(datas)
		f.close()		
	print('Insertando ' + str(fila["CODIGO_CORTO"]))
	print('------------------------------')
	datas = ''
print('***********************************')
print('Proceso de carga inicial finalizado')
print('***********************************')