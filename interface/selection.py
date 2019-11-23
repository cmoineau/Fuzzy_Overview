from tkinter import *
from affichage.affichage import save_pie, vocab
height = 600
width = 800


def prompt_fig(partition, canvas):
    save_pie(partition, '../Data/tmp.png')
    canvas.delete('all')
    canvas.create_image(0, 0, image=PhotoImage(file='../Data/tmp.png'))


def create_select_menu():
    fenetre = Tk()
    label = Label(fenetre, text="Menu de selction")
    label.pack()
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste = Listbox(fenetre)
    for i in range(len(vocab)):
        liste.insert(i+1, vocab[i])
    liste.pack()

    canv = Canvas(fenetre, bg="white", height=height, width=width)
    canv.pack()

    close_button=Button(fenetre, text="selectionner", command=lambda: prompt_fig(liste.get(ANCHOR), canv))
    close_button.pack()

    fenetre.mainloop()


if __name__ == '__main__':
    create_select_menu()