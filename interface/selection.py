from tkinter import *
from affichage.affichage import plot_pie, partition


def create_select_menu():
    fenetre = Tk()
    fenetre.title("Selection d'une partition")

    select = Frame(fenetre)
    select.pack(side=LEFT, padx=30, pady=30)
    label_select = LabelFrame(select, padx=20, pady=20, text="Terme à étudier :")
    label_select.pack(fill="both", expand="yes")

    # Creation of a list -----------------------------------------------------------------------------------------------
    liste = Listbox(label_select)
    for i in range(len(partition)):
        liste.insert(i + 1, partition[i])
    liste.pack()

    select_button = Button(select, text="Lancer la visualisation", command=lambda: plot_pie(liste.get(ANCHOR)))
    select_button.pack()

    fenetre.mainloop()


if __name__ == '__main__':
    create_select_menu()