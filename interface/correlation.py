from tkinter import *
from affichage.affichage import part_name, coeff_corell

height = 580
width = 800


def compute_correlation(param, canv):
    canv.delete('all')
    canv.create_text(width/2, height/2, text=param, font="Arial 16 italic", fill="blue", anchor=CENTER)
    dico_coef = coeff_corell(param)
    print(dico_coef)  # TODO: Catch error if element not define !


def create_correlation_menu():
    fenetre = Tk()
    fenetre.title("Visualisation de la corélation")

    label = Label(fenetre, text="Menu de correlation")
    label.pack()
    select = Frame(fenetre)
    select.pack(side=LEFT, padx=30, pady=30)
    label_select1 = LabelFrame(select, padx=20, pady=20, text="Terme à étudier :")
    label_select1.pack(fill="both", expand="yes")
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste1 = Listbox(label_select1)
    for i in range(len(part_name)):
        liste1.insert(i+1, part_name[i])
    liste1.pack()

    affiche = Frame(fenetre)
    affiche.pack(side=RIGHT, padx=30, pady=30)
    # Trying to add a canvas
    canv = Canvas(fenetre, bg="white", height=height, width=width)
    canv.pack()

    go_button = Button(select, text="selectionner", command=lambda: compute_correlation((liste1.get(ANCHOR)), canv))
    go_button.pack()

    fenetre.mainloop()


if __name__ == '__main__':
    create_correlation_menu()