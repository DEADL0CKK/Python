import sys, os, random

tab_jeu = ["pierre", "feuille", "ciseaux"]




score_ordi = 0
score_joueur = 0



while True:
    jeu = random.choice(tab_jeu)
    print(jeu)
    ok = 0

    while(ok != 1):
        print("Veuillez choisir :")
        jeu_joueurs = raw_input('Pierre (1), Feuille (2), Ciseaux (3) : ')
        print("Etes-vous sur de votre jeu ? : ")
        reponse = raw_input('Oui (1) / Non (2) : ')
        if(reponse == "1"):
            ok = 1

    if(jeu == "pierre" and jeu_joueurs == '2' or jeu == "feuille" and jeu_joueurs == '3' or jeu == "ciseaux" and jeu_joueurs == '1'):
        print("Ordi : " + jeu)
        print("Gagnez !! ")
        score_joueur = score_joueur + 1
        print("Score : ")
        print("Ordi : "+ str(score_ordi))
        print("JOueur : "+ str(score_joueur))
    else:
        print("Ordi : " + jeu)
        print("Perdu !! ")
        score_ordi = score_ordi + 1
        print("Score : ")
        print("Ordi : "+ str(score_ordi))
        print("JOueur : "+ str(score_joueur))


    print("Voulez-vous continuez la partie ?")

    continu = raw_input("Oui (1) / Non (2)")
    if(continu == '2'):
        print("Score Final :")
        print("Joueur : " + str(score_joueur))
        print("Ordi : "+ str(score_ordi))
        break

