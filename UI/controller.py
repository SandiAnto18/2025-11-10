import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillStores(self):
        stores=self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(store))

    def fillOrders(self, store_name):
        orders=self._model.getOrders(store_name)
        # PULISCO IL MENU PRECEDENTE
        self._view._ddNode.options.clear()

        # INSERISCO GLI ORDER_ID NEL MENU A TENDINA
        for order in orders:
            self._view._ddNode.options.append(
                ft.dropdown.Option(
                    key=str(order.order_id),
                    text=str(order.order_id)
                )
            )

        # ABILITO IL MENU DEGLI ORDINI
        self._view._ddNode.disabled = False

        # ABILITO IL PULSANTE CERCA
        self._view._btnCerca.disabled = False

    def handleCreaGrafo(self, e):
        store_name= self._view._ddStore.value
        k= self._view._txtIntK.value

        # costruisco il grafo sugli anni selezionati (da ,a)
        self._model.buildGraph(store_name,k)

        # Pulisco i risultati precedenti
        self._view.txt_result.controls.clear()

        # Visualizzo il numero di nodi e archi
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )
        # RECUPERO I 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5()

        self._view.txt_result.controls.append(
            ft.Text("5 archi di peso maggiore:")
        )

        # STAMPO I 5 ARCHI
        for a1, a2, w in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"Arco:{a1.order_id} -> {a2.order_id} -Peso: {w['weight']}")
            )

        self._view.update_page()
    def handleCerca(self, e):
        nodo=self._view._ddNode.value
        gruppo_nodi=self._model.getCamminoPiuLungo(nodo)
        # PULISCO I RISULTATI PRECEDENTI
        self._view.txt_result.controls.clear()

        # STAMPO IL NODO DI PARTENZA
        self._view.txt_result.controls.append(
            ft.Text(f"Nodo di partenza: {nodo}")
        )

        # STAMPO I NODI DEL CAMMINO
        for n in gruppo_nodi:
            self._view.txt_result.controls.append(
                ft.Text(n.order_id)
            )

        # AGGIORNO LA PAGINA
        self._view.update_page()

    def handleRicorsione(self, e):
        pass