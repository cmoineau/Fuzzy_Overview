from tkinter import *
from affichage.affichage import part_name, coeff_corell
from random import randint
from math import sqrt
height = 600
width = 800


def signe_alea():
    if randint(0, 1) == 1:
        signe = -1
    else:
        signe = 1
    return signe


def superpose(x, y, tab_de_coord):
    x_size = 500
    y_size = 100
    rep = False
    for coord in tab_de_coord:
        print(coord, ' | ', x, y)
        rep = coord[0]-x_size < x < coord[0]+x_size and coord[1]-y_size < y < coord[1]+y_size
    return rep


def compute_correlation(param, canv):
    canv.delete('all')
    padd = 200
    ox = width/2  # Définition du centre de la figure
    oy = height/2
    canv.create_text(ox, oy, text=param, font="Arial 12", fill="red")
    dico_coef = coeff_corell(param)
    print(dico_coef)
    tab_de_coord = []
    for key, elts in dico_coef.items():
        if elts != 'error':
            # We select a random x between -width and width
            if elts != 0:  # We do not select not correlated elements
                flag = True
                while flag:
                    rayon = ((1-elts) * oy)  # Here we compute the size of the circle
                    x = randint(int(ox - rayon), int(ox + rayon))
                    y = signe_alea() * sqrt(abs(rayon**2 - (x - ox)**2)) + oy
                    print('key : ', key, 'y : ', y, 'x : ', x)
                    canv.create_text(x, y, text=key, font="Arial 9 italic", fill="blue")
                    if not superpose(x,y, tab_de_coord):
                        flag = False
                        tab_de_coord.append((x, y))


def create_correlation_menu():
    fenetre = Tk()
    fenetre.title("Visualisation de la corélation")
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
    # create_correlation_menu()
    while(True):
        print(randint(-1,1))