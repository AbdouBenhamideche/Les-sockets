import socket 
import os 

SERVER_ADDRESS = "localhost"
SERVER_PORT = 21222
TAILLE_MAX_SEGMENT = 2048




client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


client_socket.sendto(b"SYN", (SERVER_ADDRESS, SERVER_PORT)) #demande de connexion SYN

ACK_SYN, adr = client_socket.recvfrom(TAILLE_MAX_SEGMENT)#accuse reception de demande de connexion 
if ACK_SYN == b"ACK_SYN": #si la connexion est bien établie
    client_socket.sendto(b"ACK",(SERVER_ADDRESS, SERVER_PORT))#envoi d'un accuse de réception pour confirmer l'etablissement de la connexion
    print("Connexion établie")


    fichierEnvoie = input("veuillez entrer le nom du fichier souhaité") #entrer le nom du fichire souhaitéé, il sera rechercher dans le dossier actuel si il existe il sera envoyé sinon on revoie message d'erreur 
    fichierEnvoie = fichierEnvoie.encode()
    client_socket.sendto(fichierEnvoie,(adr)) #envoi du nom du fichier au serveur



    donne_recu = b""
    numeroSegment = 0


    
    FichierExiste , addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT) #on recois le nom du fichier a rechercher l'existence
    print (FichierExiste)
    FichierExiste = (FichierExiste.decode())

    if FichierExiste == "1": #si le nom correspend 


        print("fichier trouvé")

        while True:
            data, addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT * 5) #reception de bloc de segment
            numeroSegment += 1   #on incremente le numero du bloc pour avoir le nombre total de bloc 
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



    
    
    



