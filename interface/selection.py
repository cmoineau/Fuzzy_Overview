from tkinter import *
from affichage.affichage import plot_pie, vocab



def create_select_menu():
    fenetre = Tk()
    label = Label(fenetre, text="Menu de selction")
    label.pack()
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste = Listbox(fenetre)
    for i in range(len(vocab)):
        liste.insert(i+1, vocab[i])
    liste.pack()

    close_button=Button(fenetre, text="selectionner", command=lambda: plot_pie(liste.get(ANCHOR)))
    close_button.pack()

    fenetre.mainloop()

if __name__ == '__main__':
    create_select_menu()