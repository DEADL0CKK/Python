# -*- coding: iso-8859-15 -*-
import os, sys, re

mot_a_trouver = "calcul"
vie = 6
pendu = ""
lettre_trouve = []
for i in range(len(mot_a_trouver)):
    pendu = pendu + "_"

print(pendu) 
while True:
    lettre = raw_input("Veuillez donnez une lettre dans le mot : ")

    if(lettre in mot_a_trouver):
        print("Bravo, vous avez trouvé une lettre !!!")
        for i in mot_a_trouver:
            if(lettre == i ):
                lettre_trouve += lettre
    else:
        print("Faux, tu perds un point !!")
        vie = vie - 1
            
    if(len(lettre_trouve) == len(mot_a_trouver) ):
        print("Victoire")
        break
    else:
        print("Vous avez trouvé :")
        print(lettre_trouve)
        print("Il vous reste : "+ str(vie) + " de point de vie")

    if vie == 0:
        print("Vous avez perdu ciao !!!!")
        break