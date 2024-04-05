import socket 
import os 

SERVER_ADDRESS = "localhost"
PORT = 21222
TAILLE_MAX_SEGMENT = 2048
N = 5
nombreDeTentative = 5


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
                
                
                if n == N:
                    sock.sendto(blocSegment, addr)
                    for i in range(nombreDeTentative):
                        try:
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
                        print("Aucun accusé de réception reçu après {} tentatives, déclenchant le timeout.".format(nombreDeTentative))



                    blocSegment = b""
                    n = 0

            if blocSegment:
                sock.sendto(blocSegment, addr)  # envoyer ce que reste
                try:
                        server_socket.settimeout(3)
                        msg, adr = sock.recvfrom(TAILLE_MAX_SEGMENT)  #accuse la reception de chaque bloc
                        if  msg == b"BlocSegmentRecu":
                            print ("accusé de reception recu pour un bloc de segments")
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

print("le serveur est en attente et sur écoute " )

while True:
    data, client_address = server_socket.recvfrom(TAILLE_MAX_SEGMENT) 
    if data == b"DEMANDE DE CONNEXION":
        print("connexion établie")
        server_socket.sendto(b"CONNECTION RECUE",client_address)
        nomFile, client_address = server_socket.recvfrom(TAILLE_MAX_SEGMENT)
        v = rechercher_fichier(nomFile.decode())
        server_socket.sendto((str(v).encode()), client_address)
        if v:
            SendFile(server_socket, client_address,  nomFile.decode())
            break
        else:
            break
            
    else:
        print("Connexion non établie")
        break

    



    



    

    