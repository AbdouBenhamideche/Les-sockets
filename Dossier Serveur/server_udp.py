import socket 
import os 
import hashlib

SERVER_ADDRESS = "localhost"
PORT = 21222
TAILLE_MAX_SEGMENT = 2048
NOMBRE_SEGMENTS_BLOC = 5
NOMBRE_TENTATIVE = 5

def calculate_file_hash(file_path): #pour calculer l'hachage d'un fichier 
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # Lecture par blocs de 64 Ko
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def rechercher_fichier(nom_fichier):
    # Récupérer le chemin absolu du répertoire actuel

    chemin_repertoire = os.getcwd()
    
    # Vérifier si le fichier existe dans le répertoire actuel
    if nom_fichier in os.listdir(chemin_repertoire):
        print (f"Le fichier '{nom_fichier}' a été trouvé dans le répertoire actuel.")
        return 1
    else:
        print (f"Le fichier '{nom_fichier}' n'a pas été trouvé dans le répertoire actuel.")
        return 0


def  SendFile(sock, addr, nomFichier):
    try:
        with open(nomFichier, 'rb') as file:
            blocSegment = b""
            n = 0
            
            while True:
                segment = file.read(TAILLE_MAX_SEGMENT)
                if not segment:
                    break
                
                blocSegment += segment
                n += 1
                
                
                if n == NOMBRE_SEGMENTS_BLOC:
                    
                    for i in range(NOMBRE_TENTATIVE):
                        try:
                            sock.sendto(blocSegment, addr)
                            server_socket.settimeout(3)
                            msg, adr = server_socket.recvfrom(TAILLE_MAX_SEGMENT)  #accuse la reception de chaque bloc
                            if msg == b"BlocSegmentRecu":
                                print("Accusé de réception reçu pour un bloc de segments")
                                break  # Sort de la boucle si le message est reçu avec succès
                        

                            
                            
                            
                        except socket.timeout:
                            print("Délai d'attente a expiré (tentative {}/5)".format(i + 1))
                        except Exception as e:
                            print("Erreur:", e)





                    else:
                        print("Aucun accusé de réception reçu après {} tentatives, déclenchant le timeout.".format(NOMBRE_TENTATIVE))



                    blocSegment = b""
                    n = 0

            if blocSegment:
                for i in range(NOMBRE_TENTATIVE):
                    try:
                        sock.sendto(blocSegment, addr)  # envoyer ce que reste (inf a 5 segments)
                        try:      
                            server_socket.settimeout(3)
                            msg, adr = sock.recvfrom(TAILLE_MAX_SEGMENT)  #accuse la reception de chaque bloc
                            if  msg == b"BlocSegmentRecu":
                                print ("accusé de reception recu pour un bloc de segments")
                        except socket.timeout:
                            print("Délai d'attente a expiré")

                        except Exception as e:
                            print("erreur")
                        
                
                
                    
                    except socket.timeout:
                            print("Délai d'attente a expiré")

                    except Exception as e:
                            print("erreur")


            sock.sendto(b"TERMINE", addr)
            print("Fichier envoyé avec succès")
    except OSError as e:
        if e.errno == 10040:
            print("Erreur: La taille du message dépasse la limite du tampon de socket. Essayez de réduire la taille du message ou d'augmenter la taille du tampon.")
        else:
            print("Erreur:", e)




server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, PORT))

print("le serveur est en attente et sur écoute " )  #mettre le serveur sur ecoute

while True:
    SYN, client_address = server_socket.recvfrom(TAILLE_MAX_SEGMENT) #recevoir la demande de connexion du client
    if SYN == b"SYN":
        print("Demande de connexion recu")
        server_socket.sendto(b"ACK_SYN",client_address) #ACK-SYN

        ACK, adr = server_socket.recvfrom(TAILLE_MAX_SEGMENT)

        if ACK == b"ACK":
            print("Connexion établie")

            nomFile, client_address = server_socket.recvfrom(TAILLE_MAX_SEGMENT) #recevoir le nom du fichier souhaiter recuperer de la part du client 
            FichierExiste = rechercher_fichier(nomFile.decode()) #fonction qui verifie  si le fichier existe ou non !!!a partir du chemin de l'execution du script!!!
            server_socket.sendto((str(FichierExiste).encode()), client_address)#envoyer le resultat de l'existence du fichier au client
            if FichierExiste:
                SendFile(server_socket, client_address,  nomFile.decode()) #envoie du fichier avec la fonction SendFile
                server_socket.sendto(calculate_file_hash(nomFile.decode()).encode(), client_address) #envoie de l'hachage du fichier avant l'envoie
                
                break
            else:
                break
        else: 
            print("Connexion non établie")
            
    else:
        print("Connexion non établie")
        break   

    


