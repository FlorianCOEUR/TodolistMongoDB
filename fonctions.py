
# Ajouter une tâche
# Compléter une tâche (la marquer comme terminée avec la date du jour)
# Supprimer une tâche
# Mettre à jour une tâche
from pymongo import MongoClient
import datetime
import sqlite3

client = MongoClient('mongodb://localhost:27017/')
db=client["DW1"]
todolist=db["todolist"]
filter={}
tasks = client['DW1']['todolist'].find(
  filter=filter
)

#fonction récursive du menu
def menu():
    print("Bienvenue sur la gestion de ta ToDo List!")
    print("------------------------------------------")
    print("Que souhaitez vous faire?")
    print("------------------------------------------")
    print("-1 Afficher les tâches")
    print("------------------------------------------")
    print("-2 Ajouter une tâche")
    print("------------------------------------------")
    print("-3 Compléter une tâche")
    print("------------------------------------------")
    print("-4 Supprimer une tâche")
    print("------------------------------------------")
    print("-5 Mettre à jour une tâche")
    print("------------------------------------------")
    choix=int(input("Entrez votre choix\n"))
    match choix:
        case 1:
            afficherTaches(1)
        case 2:
            ajouterTache()
        case 3:
            finirTache()
        case 4:
            suppTache()
        case 5:
            print("En cours de Dev")
        case _:
            quit=input("Choix invalide!\nSouhaitez vous quittez la gestion? (y/n?)\n")
            if quit!="y":
                menu()
            else:
                end()
#Fin du programme
def end():
    print("Merci d'avoir utiliser ce programme\nRedirection vers mon linkedin ;)")

#Fonction de fin de fonction
def fonctionFin():
    choix=input("Que faire ensuite?\nMenu principal? (m / M)\nQuitter la gestion (q / Q)?\n")
    match choix.lower():
        case "m":
            menu()
        case "q":
            end()
        case _:
            print("Choix non pris en compte!")
            fonctionFin()

#Fonction pour afficher les tâches

def afficherTaches(state):
    if state == "0":
        i=1
        for tache in todolist.find():
            match int(tache["statut"]):
                case 1:
                    statutType="A faire"
                case 2:
                    statutType="En cours"
                case 3:
                    statutType="Terminée"
            print(i," ",tache["nom"],": ",statutType)
            i+=1
        fonctionFin()
    else:
        print("Quelles tâches souhaitez vous afficher?")
        state=input(" -Toutes les tâches? (0)\n -Les tâches à faire? (1)\n -Les tâches en cours? (2)\n -Les tâches terminées? (3)\n")
        match state:
            case "0":
                afficherTaches("0")
            case "1":
                for tache in todolist.find({"statut":1}):
                    print(tache["nom"],": A faire")
                fonctionFin()
            case "2":
                for tache in todolist.find({"statut":2}):
                    print(tache["nom"],": En cours")
                fonctionFin()
            case "3":
                for tache in todolist.find({"statut":3}):
                    print(tache["nom"],": Terminée")
                fonctionFin()
            case _:
                print("Choix impossible")
                afficherTaches("1")

    
    

#Fonction pour ajouter une tâche

def ajouterTache():
    nomTache= input("Indiquer le nom de la nouvelle tâche:\n")
    numStatut=statutDemande()
    todolist.insert_one({
        "nom" : nomTache,
        "statut" : numStatut}
    )
    fonctionFin()

#Fonction pour demander le statut de la tâche
def statutDemande():
    statut=input("et le statut : ('A faire', 'En cours' ou 'Terminee')\n")
    match statut.lower():
        case "a faire":
            numStatut=1
        case "en cours":
            numStatut=2
        case "terminee":
            numStatut=0
        case _:
            print("Choix non pris en compte")
            numStatut=statutDemande()
    return numStatut

#Fonction pour définir une tache comme terminée

def finirTache():
    afficherTaches()
    date=datetime.date.today()
    tache=int(input())
    tasks = client['DW1']['todolist'].find(
        filter=filter
    )
    rows=list(tasks)
    supp=int(input("choisir la tâche à finir:"))
    while 0>=tache or tache>=len(rows):
        print("La tâche à modifier n'existe pas!")
        tache=int(input("Choisir la tâche à finir:"))
    i=1
    for task in tasks:
        if i==tache:
            nomTache=task["nom"]
            query={"nom": nomTache}
            client["DW1"]["todolist"].update_one(query,{
                "$set": {"statut" : "Terminer"}
            })
            client["DW1"]["todolist"].update_one(query,{
                "$set": {"date" : str(date)}
            })
        i+=1



# Supprimer une tâche

def suppTache():
    afficherTaches()
    tasks = client['DW1']['todolist'].find(
        filter=filter
    )
    rows=list(tasks)
    supp=int(input("choisir la tâche à supprimer:"))
    while 0>=supp or supp>=len(rows):
        print("La tâche à supprimer n'existe pas!")
        supp=int(input("Choisir la tâche à supprimer:"))
    i=1
    for task in tasks:
        if i==supp:
            nomTache=task["nom"]
            query={"nom": nomTache}
            client["DW1"]["todolist"].delete_one(query)
        i+=1


#Mettre à jour une tache
def majTache():
    afficherTaches()
    maj=int(print("Quelle tâche souhaitez vous mettre à jour?"))


