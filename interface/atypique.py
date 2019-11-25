from tkinter import *
from affichage.affichage import partition, coeff_corell, coeff_atyp
from random import randint
from math import sqrt

height = 600
width = 800
R = 100  # taille max d'un cercle



def superpose(x, y, r, tab_de_coord):
    rep = False
    for coord in tab_de_coord:
        x0, y0 = coord[0], coord[1]
        r0 = coord[2]
        D = sqrt((x - x0) ** 2 + (y - y0) ** 2)
        print(coord, ' | ', x, y, r)
        if D <= R * r0:
            rep = True
    return rep


def compute_atypique(param, canv):
    canv.delete('all')
    dico_coef = coeff_atyp(param)
    print(dico_coef)
    tab_de_coord = []
    color_list = ['red', 'blue', 'green', 'yellow', 'orange', 'indigo', 'purple', 'grey', 'cyan', 'maroon', 'gold',
                  'pink']
    color_used = [False] * len(color_list)
    for key, elts in dico_coef.items():
        if elts != 'error':
            # We select a random x between -width and width
            if elts != 0:  # We do not select not correlated elements
                overlap = True
                while overlap:
                    r = elts  # Here we compute the size of the circle
                    x = randint(int(r * R) + 50, int(width - r * R) - 50)
                    y = randint(int(r * R) + 50, int(height - r * R) - 50)

                    print('key : ', key, 'y : ', y, 'x : ', x)
                    if not superpose(x, y, r, tab_de_coord):
                        k = randint(0, len(color_list)-1)
                        while not (color_used[k]):
                            k = randint(0, len(color_list) - 1)
                        color = color_list[k]
                        color_used[k]=True
                        canv.create_oval(x - r * R, y - r * R, x + r * R, y + r * R, bg= color)
                        canv.create_text(x, y, text=key + "\n\t" + str(int(elts * 100)) + "%", font="Arial 9 italic",fill="black")

                        overlap = False
                        tab_de_coord.append((x, y, r))


def create_atypique_menu():
    fenetre = Tk()
    fenetre.title("Visualisation des caractères atypiques")
    select = Frame(fenetre)
    select.pack(side=LEFT, padx=30, pady=30)
    label_select1 = LabelFrame(select, padx=20, pady=20, text="Terme à étudier :")
    label_select1.pack(fill="both", expand="yes")
    # Creation of a list -----------------------------------------------------------------------------------------------
    liste1 = Listbox(label_select1)
    for i in range(len(partition)):
        liste1.insert(i + 1, partition[i])
    liste1.pack()

    affiche = Frame(fenetre)
    affiche.pack(side=RIGHT, padx=30, pady=30)
    # Trying to add a canvas
    canv = Canvas(fenetre, bg="white", height=height, width=width)
    canv.pack()

    go_button = Button(select, text="selectionner", command=lambda: compute_atypique((liste1.get(ANCHOR)), canv))
    go_button.pack()

    fenetre.mainloop()
