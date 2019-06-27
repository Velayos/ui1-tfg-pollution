#/bin/bash



python3 generacion.py

cd ./json
for jsonFile in *.json
do
	echo ${jsonFile}
	curl -X POST -H "Content-Type: application/json" -d @${jsonFile}  "http://localhost:8080/FROST-Server/v1.0/Things"
done

~

