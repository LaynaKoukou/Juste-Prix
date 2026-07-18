import random
from tkinter import *
from tkinter import ttk
import pygame


nombreADeviner = random.randint(1, 500)
propositions = []


fenetre = Tk()
fenetre.title("Le juste prix !")
fenetre.config(bg="#87CEEB")
fenetre.geometry("720x480")
fenetre.image_names = ['juste-prix-1.jpg']

fenetre.update_idletasks()
w = fenetre.winfo_width()
h = fenetre.winfo_height()
ws = fenetre.winfo_screenwidth()
hs = fenetre.winfo_screenheight()
x = (ws - w) // 2
y = (hs - h) // 2
fenetre.geometry(f"{w}x{h}+{x}+{y}")




texteBienvenue = Label(fenetre, text="", font=("Arial", 14), justify=CENTER, bg="#87CEEB")
texteBienvenue.pack(pady=40)

def defilementTexte(texte, index=0, texteAffiche=""):
    if index < len(texte):
        texteAffiche += texte[index]
        texteBienvenue.config(text=texteAffiche)
        fenetre.after(40, defilementTexte, texte, index + 1, texteAffiche)

defilementTexte(
    "Bienvenue dans le juste prix ! "
    "Le prix à deviner est compris entre 1 et 500. "
)

message = Label(fenetre, text="Appuie sur démarrer pour commencer.", font=("Arial", 12), justify=CENTER, fg="black", bg="#87CEEB")
message.pack(pady=10)

saisie = Entry(fenetre, font=("Arial", 14), justify="center")
saisie.pack(pady=6)
saisie.focus_set()

temps_restant = 30
timer_id = None
decompte_id = None


def evaluationPrix(event=None):

    if str(boutonProposer['state']) == 'disabled':
        return
    try:
        proposition = int(saisie.get())
        

        if proposition < nombreADeviner:
            message.config(text="C'est plus !")
        elif proposition == nombreADeviner:
            message.config(text="Bravo ! C'était le bon nombre.")
            boutonProposer.config(state=DISABLED)
            fenetre.config(bg="#7adb30")
            texteBienvenue.config(bg="#7adb30")
            message.config(bg="#7adb30")
            label_decompte.config(bg="#7adb30")
            label_timer.config(bg="#7adb30")
            arreter_timer()
            # if HAVE_SOUND: sonVictoire.play()
        else:
            message.config(text="C'est moins !")
    except ValueError:
        message.config(text="Erreur : entre un nombre entier.")
    finally:
        saisie.delete(0, END)
        saisie.focus_set()

def arreter_timer():
    global timer_id
    if timer_id is not None:
        fenetre.after_cancel(timer_id)
        timer_id = None

def annuler_decompte():
    global decompte_id
    if decompte_id is not None:
        fenetre.after_cancel(decompte_id)
        decompte_id = None
        label_decompte.config(text="")

def resetJeu():
    global essai, nombreADeviner, propositions, temps_restant
    propositions = []
    nombreADeviner = random.randint(1, 500)
    message.config(text="Appuie sur Démarrer pour commencer.", fg="black")
    saisie.delete(0, END)
    boutonProposer.config(state=DISABLED)
    boutonDemarrer.config(state=NORMAL)
    fenetre.config(bg="#87CEEB")
    message.config(bg="#87CEEB")
    label_decompte.config(bg="#87CEEB")
    texteBienvenue.config(bg="#87CEEB")
    
    arreter_timer()
    annuler_decompte()
    temps_restant = 30
    label_timer.config(text="Temps restant : 30 s", fg="black", bg="#87CEEB")
    saisie.focus_set()

boutonProposer = Button(fenetre, text="Proposer", font=("Arial", 12), command=evaluationPrix)
boutonProposer.pack(pady=6)
boutonProposer.config(state=DISABLED)

boutonReset = Button(fenetre, text="Réinitialiser la partie", font=("Arial", 12), command=resetJeu)
boutonReset.pack(pady=6)

saisie.bind("<Return>", evaluationPrix)

label_decompte = Label(fenetre, text="", font=("Arial", 18, "bold"), bg="#87CEEB")
label_decompte.pack(pady=4)

label_timer = Label(fenetre, text="Temps restant : 30 s", font=("Arial", 12),bg="#87CEEB")
label_timer.pack(pady=4)

boutonDemarrer = Button(fenetre, text="Démarrer", font=("Arial", 12))
boutonDemarrer.pack(pady=6)

def tick_timer():
    global temps_restant, timer_id
    if temps_restant <= 0:
        label_timer.config(text="Temps écoulé !")
        message.config(
            text=f"Perdu ! Le nombre à deviner était {nombreADeviner}.", fg="red"
            
            
                
        )
        boutonProposer.config(state=DISABLED)
        timer_id = None
        return
    label_timer.config(
        text=f"Temps restant : {temps_restant} s",
        fg=("red" if temps_restant <= 5 else "black")
    )
    temps_restant -= 1
    timer_id = fenetre.after(1000, tick_timer)

def demarrer_temps(duree=30):
    global temps_restant, timer_id
    if timer_id is not None:
        fenetre.after_cancel(timer_id)
    temps_restant = duree
    label_timer.config(text=f"Temps restant : {temps_restant} s",fg="black",)
    timer_id = fenetre.after(1000, tick_timer)

def demarrer_decompte(val=3):
    global decompte_id
    
    boutonProposer.config(state=DISABLED)
    boutonDemarrer.config(state=DISABLED)
    message.config(text="Prépare-toi...",)

    if val <= 0:
        label_decompte.config(text="Go !")
        message.config(text="Propose un nombre.")
        boutonProposer.config(state=NORMAL)   # Autoriser à jouer maintenant
        demarrer_temps(30)                    # Lancer le chrono
        decompte_id = fenetre.after(1000, lambda: label_decompte.config(text=""))
        return

    label_decompte.config(text=str(val))
    decompte_id = fenetre.after(1000, demarrer_decompte, val - 1)

boutonDemarrer.config(command=lambda: demarrer_decompte(3))


fenetre.mainloop()
