import requests
import pandas as pd
import time

def getIdObservationToAdd(obsName):
#funcion que devuelve el id al que debemos asignar los datos recuperados
	baseUrl = "http://localhost:8080/FROST-Server/v1.0"
	url = baseUrl + '/' + 'Datastreams'

	# Load name and id of present datastreams
	ds = requests.get(url + '?$select=name,id').json()
	for i in ds:
		if i.get('name') == obsName:
			return ds[i].id
	return()


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

sendingDatastreamID = None

#en df2 tengo todos los datos con las mediciones de la última hora
#recorro df2 construyendo json y cargando los datos en frost

print(df2.count)
for index, row in df2.iterrows():
	ultimaObservacion = '{"phenomenonTime":'+str(row['AÑO'])+ '-' + str(row['MES']) + '-' + str(row['DIA'])+'T'+horaConsultada[1:None]+':00:00Z","result":"'+ str(row[horaConsultada])+'"}'
	print(getIdObservationToAdd(row))



# Empty variable for holding the target datastream id
'''
sendingDatastreamID = None
for stream in dataStreams['value']:	
    datastreamID = stream['@iot.id']
    datastreamName = stream['name']
    #construyo la hora en qaue se ha realizado la medición que vamos a insertar en el servidor FROST
    # EJEMPLO: phenomenonTime": "2019-03-14T10:00:00Z","result": 21.0    
    datos = datastreamName.split(' en ', 1)
    unidadMedida = datos[0]
'''

