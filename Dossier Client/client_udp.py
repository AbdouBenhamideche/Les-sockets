import socket 
import os 
import hashlib

SERVER_ADDRESS = "localhost"
SERVER_PORT = 21222
TAILLE_MAX_SEGMENT = 2048


def calculate_file_hash(file_path): #pour calculer l'hachage d'un fichier 
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # Lecture par blocs de 64 Ko
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()



client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


client_socket.sendto(b"SYN", (SERVER_ADDRESS, SERVER_PORT)) #demande de connexion SYN

ACK_SYN, adr = client_socket.recvfrom(TAILLE_MAX_SEGMENT)#accuse reception de demande de connexion 
if ACK_SYN == b"ACK_SYN": #si la connexion est bien établie
    client_socket.sendto(b"ACK",(SERVER_ADDRESS, SERVER_PORT))#envoi d'un accuse de réception pour confirmer l'etablissement de la connexion
    print("Connexion établie")


    fichierEnvoie = input("veuillez entrer le nom du fichier souhaité:  ") #entrer le nom du fichire souhaitéé, il sera rechercher dans le dossier actuel si il existe il sera envoyé sinon on revoie message d'erreur 
    fichierEnvoie = fichierEnvoie.encode()
    client_socket.sendto(fichierEnvoie,(adr)) #envoi du nom du fichier au serveur



    donne_recu = b"" #variable qui va stocker les données recu
    numeroSegment = 0  #pour calculer et afficher le nombre de bloc de segments 


    
    FichierExiste , addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT) #on recois si le fichier existe ou pas
    print (FichierExiste) #juste pour tester
    FichierExiste = (FichierExiste.decode())

    if FichierExiste == "1": #si le nom correspend 


        print("fichier trouvé")

        while True:
            data, addr = client_socket.recvfrom(TAILLE_MAX_SEGMENT * 5) #reception de bloc de segment, le x5 c'est psq le bloc contient 5 segments au plus 
            numeroSegment += 1   #on incremente le numero du bloc pour avoir le nombre total de bloc 
            client_socket.sendto(b"BlocSegmentRecu",addr) #accusé de reception pour chaque bloc
            print("bloc de segment " + str(numeroSegment) + " recu avec succées")
            if data == b"TERMINE":
                break

            donne_recu += data

        with open(fichierEnvoie.decode(),"wb") as file :
            file.write(donne_recu)
        print("fichier recu avec succée")
        
      
        hashFileServer,adr = client_socket.recvfrom(TAILLE_MAX_SEGMENT)# on récupère l'hachage du fichier se trouvant au niveau du serveur
        hashFileServer = hashFileServer.decode()
       
        hashFileClient = calculate_file_hash(fichierEnvoie) #hachage du fichier apres la reception  
        if hashFileClient == hashFileServer:  #si les deux hachage sint indentique donc les données sont integrées
            print("Le fichier est intègre.")
        else:
            print("Le fichier a été altéré lors de la transmission.")
          
       
        
       
        
    else:
        print("le fichier n'existe pas.")    #si le nom ne correspond pas






else:     #si y avais pas d accusé de reception de connexion recu
    print("Erreur de connection")



    
    
    



