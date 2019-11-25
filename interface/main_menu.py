from tkinter import *
from tkinter.messagebox import *
from interface.selection import create_select_menu
from interface.correlation import create_correlation_menu
from interface.correlation2 import create_correlation2_menu
from interface.atypique import create_atypique_menu


def not_ready_yet():
    """
    A small alert to inform the user that something is not ready yet.
    :return:
    """
    showerror("Erreur : Page pas prêtes", "La page est actuellement en construction !")


def create_main_menu():
    # Initialisation of the window -------------------------------------------------------------------------------------
    fenetre = Tk()
    fenetre.title("Visualisation des données de l'aéoport")
    # End of the window ------------------------------------------------------------------------------------------------

    # Creation of the selection menu -----------------------------------------------------------------------------------
    label_main = LabelFrame(fenetre, padx=20, pady=20, text="Menu de selection")
    label_main.pack(fill="both", expand="yes")

    selection_button = Button(label_main, text="Étude d'une partition", command=create_select_menu)
    selection_button.pack()

    correlation_button = Button(label_main, text="Corrélation d'une partition avec les autres", command=create_correlation_menu)
    correlation_button.pack()

    correlation_button = Button(label_main, text="Corrélation entre deux partitions",
                                command=create_correlation2_menu)
    correlation_button.pack()

    atypique_button = Button(label_main, text="Terme Atypique", command=create_atypique_menu)
    atypique_button.pack()
    # End of the selection menu ----------------------------------------------------------------------------------------

    close_button=Button(fenetre, text="Fermer", command=fenetre.quit)
    close_button.pack()

    # Running the main window ------------------------------------------------------------------------------------------
    fenetre.mainloop()


if __name__ == '__main__':
    create_main_menu()