# -*- coding: iso-8859-15 -*-
import sys, random, os

juste_prix = random.randint(1, 10000)
print(juste_prix)
point_final= 1000

while True:
    ligne = raw_input('Entrez un prix : ')
    prix_joueurs = int(ligne)



    if prix_joueurs == juste_prix:
        print("Bravo, c'est gagné !!")
        print("votre score est " + str(point_final))
        break
    elif (prix_joueurs > juste_prix):
        print("Plus Petit que " + ligne)
        point_final = point_final-100
        if(point_final == 0):
            print("Partie Perdue !!!")
            break

    elif (prix_joueurs< juste_prix):
        print("Plus grand que " + ligne)
        point_final = point_final - 100
        if(point_final == 0):
            print("Partie Perdue !!!")
            break

