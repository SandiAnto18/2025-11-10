import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)

    # CARICO GLI ELEMENTI GRAFICI DELLA VIEW
    my_view.load_interface()

    # RIEMPO IL DROPDOWN CON GLI STORE PRESI DAL DATABASE
    my_controller.fillDDStores()


ft.app(target=main)
