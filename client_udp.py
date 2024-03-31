import socket 
import os 

SERVER_ADDRESS = "localhost"
SERVER_PORT = 21222
TAILLE_MAX_SEGMENT = 1024

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


client_socket.sendto(b"DEMANDE DE CONNEXION", (SERVER_ADDRESS, SERVER_PORT)) #demande de connexion

donne_recu = b""
numeroSegment = 0
while True:
    data, addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT) 
    numeroSegment += 1
    print("segment " + str(numeroSegment) + " recu avec succées")
    if data == b"TERMINE":
        break

    donne_recu += data

with open("FichierRecu.bin" ,"wb") as file :
    file.write(donne_recu)
print("fichier recu avec succée")



    
    
    



