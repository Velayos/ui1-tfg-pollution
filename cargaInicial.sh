#/bin/bash

curl -X DELETE -H "Content-Type: application/json" -H -d '' "http://localhost:8080/FROST-Server/v1.0/MultiDatastreams"
curl -X DELETE -H "Content-Type: application/json" -H -d '' "http://localhost:8080/FROST-Server/v1.0/Datastreams"
curl -X DELETE -H "Content-Type: application/json" -H -d '' "http://localhost:8080/FROST-Server/v1.0/Locations"
curl -X DELETE -H "Content-Type: application/json" -H -d '' "http://localhost:8080/FROST-Server/v1.0/Sensors"
curl -X DELETE -H "Content-Type: application/json" -H -d '' "http://localhost:8080/FROST-Server/v1.0/Things"

python3 generacion.py

cd ./json
for jsonFile in *.json
do
	echo ${jsonFile}
	curl -X POST -H "Content-Type: application/json" -d @${jsonFile}  "http://localhost:8080/FROST-Server/v1.0/Things"
	echo "introducido " ${jsonFile}
done

cd ..