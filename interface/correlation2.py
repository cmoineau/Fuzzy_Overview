from tkinter import *
from affichage.affichage import vocab, plot_heat_map


def create_correlation2_menu():
    fenetre = Tk()
    fenetre.title("Visualisation de la corrélation")
    select = Frame(fenetre)
    select.pack(side=LEFT, padx=30, pady=30)
    label_select1 = LabelFrame(select, padx=20, pady=20, text="Partition à étudier :")
    label_select1.pack(fill="both", expand="yes")

    label_terme1 = Label(label_select1, text="1er partition :")
    label_terme1.pack()
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste1 = Listbox(label_select1)
    for i in range(len(vocab)):
        liste1.insert(i+1, vocab[i])
    liste1.pack()

    label_terme2=Label(label_select1, text="2ème partition :")
    label_terme2.pack()
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste2 = Listbox(label_select1)
    for i in range(len(vocab)):
        liste2.insert(i + 1, vocab[i])
    liste2.pack()

    go_button = Button(select, text="Lancer la recherche de corrélation !", command=lambda: plot_heat_map((\
        liste1.get(ANCHOR)), liste2.get(ANCHOR)))
    go_button.pack()

    fenetre.mainloop()


if __name__ == '__main__':
    create_correlation2_menu()