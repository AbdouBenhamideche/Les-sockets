import socket 
import os 

SERVER_ADDRESS = "localhost"
SERVER_PORT = 21222
TAILLE_MAX_SEGMENT = 2048




client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


client_socket.sendto(b"DEMANDE DE CONNEXION", (SERVER_ADDRESS, SERVER_PORT)) #demande de connexion

dn, adr = client_socket.recvfrom(TAILLE_MAX_SEGMENT)#accuse reception de demande de connexion 
if dn == b"CONNECTION RECUE": #si la connexion est bien établie

#
    fichierEnvoie = input("veuillez entrer le nom du fichier souhaité") #entrer le nom du fichire souhaitéé, il sera rechercher dans le dossier actuel si il existe il sera envoyé sinon on revoie message d'erreur 
    fichierEnvoie = fichierEnvoie.encode()
    client_socket.sendto(fichierEnvoie,(adr)) #envoi du nom du fichier a envoyer au serveur



    donne_recu = b""
    numeroSegment = 0


    
    V , addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT)
    print (V)
    V = (V.decode())

    if V == "1": #si le nom correspend 


        print("fichier trouvé")

        while True:
            data, addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT * 5) 
            numeroSegment += 1
            client_socket.sendto(b"BlocSegmentRecu",addr) #accusé de reception pour chaque bloc
            print("bloc de segment " + str(numeroSegment) + " recu avec succées")
            if data == b"TERMINE":
                break

            donne_recu += data

        with open("FichierRecu.bin" ,"wb") as file :
            file.write(donne_recu)
        print("fichier recu avec succée")
    else:
        print("le fichier n'existe pas.")    #si le nom ne correspond pas






else:     #si y avais pas d accusé de reception de connexion recu
    print("Erreur de connection")



    
    
    



