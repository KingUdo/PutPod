# PutPod

PutPod is a file upload "Honeypot" which takes advantage of adversaries scannign the internet for websites which accept fileupload via PUT to place malware on those for future campaigns.
I noticed the baviour of a remote ip trying to PUT a file onto my webserver and straight after sening a GET request for exactly that file. Initally I thought that this must be scannig activcity from bugbounty hunters, but wasn't 100% sure, so I had to find out what type of file is beeing uploaded. 
Of casue I didn't want to distrubute malware from my domain so I needed to build somehting that is accepting put request and deliving the same file back to the external IP withough distributing the file to any other requesters (potentialy victims of the malware campain). PutPod provides that behaviour. It's a super simple flask docker container which accepts PUT request, stores the files on disk and saves the remote IP which send the PUT request to a sqlite database. If the same IP tryies to GET the file it PutPod will deliver it, otherwise it will just return a 404. To make my live a bit easyer I have offloaded the TLS encryption/decryption part to a haproxy docker.

# Building
To build the PutPod docker just run the Makefile in the PutPod directory. This will build the docker and tag it with putpod:latest. Once the putpod docker is build and uploded to the server where you want to deploy the system you will have to get yourself a TLS certificate (I usually use letsencrpyt) and store that one in the `certs` folder, as well as adjust the `haproxy.cfg` in the TLS frontent part to know the name of your tls certificate. Once that's done you can just run the docker-compose.yml file and the whole thing will spin up. 

# Malware
To check which malware you collected, you need to look into the `malware` folder. In there all files will be stored with their md5 hash value (which you can for example put into VirusTotal to check). Additonaly you can check where the file came from by looking into the putpod.db with `sqlite3 putpod.db` and then `select * from files;`. This will display you all files which were uploaded as well as their original upload name, timestamp and the source IP.
