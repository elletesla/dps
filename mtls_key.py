import socket
import subprocess
import os

def run(cmd):
    print("Running In Shell")
    subprocess.run(cmd,check=True,shell=True)

def generate_cert():
    #generating CA.key
    run("openssl genrsa -out ca.key 4096")
    run("openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj /C=IN/ST=TN/L=Coimbatore/O=LabCA/OU=Root/CN=MyRootCA")
    run("openssl genrsa -out server.key 2048")
    run("openssl req -new -key server.key -out server.csr -subj /C=IN/ST=TN/L=Coimbatore/O=LabCA/OU=Root/CN=server")
    run("openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 ")
    run("openssl genrsa -out client.key 2048")
    run("openssl req -new -key client.key -out client.csr -subj /C=IN/ST=TN/L=Coimbatore/O=LabCA/OU=Root/CN=client")
    run("openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 ")



generate_cert()
