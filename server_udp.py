import socket 
import os 

SERVER_ADDRESS = "localhost"
PORT = 21222
TAILLE_MAX_SEGMENT = 1024

def  SendFile(sock, addr, nomFichier):
    with open(nomFichier, 'rb') as file:
        while True:
            segment =  file.read(TAILLE_MAX_SEGMENT)

            if not segment:
                break

            sock.sendto(segment, addr)
            msg, adr = sock.recvfrom(TAILLE_MAX_SEGMENT) #accuse de recepption pour chaque segment !!!!!!
        sock.sendto(b"TERMINE", addr)
        print("fichier envoyé avec succée")




server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, PORT))
print("le serveur est en attente et sur écoute " )

while True:
    data, client_address = server_socket.recvfrom(TAILLE_MAX_SEGMENT) 
    if data == b"DEMANDE DE CONNEXION":
        print("connexion établie")
        server_socket.sendto(b"CONNECTION RECUE",client_address)
        SendFile(server_socket, client_address,  'testfile.txt')
        break
    else:
        print("Connexion non établie")
        break

    



    



    

    