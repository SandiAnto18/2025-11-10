import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        store = self._model.getStores()

        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(s))

        self._view.update_page()

    def handleCreaGrafo(self, e):

        ## RECUPERO LO STORE SELEZIONATO E IL VALORE K INSERITO DALL'UTENTE nella VIEW
        self._model.buildGraph(self._view._ddStore.value,self._view._txtIntK.value)
        # SVUOTO IL RISULTATO PRECEDENTE
        self._view.txt_result.controls.clear()
        # comando per aggiungere righe testuali/numero in output
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{self._model.getNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{self._model.getEdges()}"))
        self._view.update_page()
    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass