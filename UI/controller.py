import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._annoSelezionato = None
        self._squadraSelezionata = None
    def handleCreaGrafo(self, e):
        if self._annoSelezionato is None:
            self._view._txt_result.clean()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un anno!",color="red"))
            self._view.update_page()
            return
        self._model.buildGraph()
        self._view._txt_result.clean()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"{self._model._graph}", color="green"))

        self._view.update_page()
        return

    def handleDettagli(self, e):
        if self._squadraSelezionata is None:
            self._view._txt_result.clean()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare una squadra!", color="red"))
            self._view.update_page()
            return

        if not self._model.esisteGrafo():
            self._view._txt_result.clean()
            self._view._txt_result.controls.append(ft.Text(f"Creare un grafo!", color="red"))
            self._view.update_page()
            return

        dettagli = self._model.getDettagliGrafo(self._squadraSelezionata)

        self._view._txt_result.clean()
        self._view._txt_result.controls.append(ft.Text(f"Di seguito l'elenco delle squadre adiacenti a {self._squadraSelezionata}"))

        for d in dettagli:

            self._view._txt_result.controls.append(ft.Text(f"{d[0]} - {d[1]}"))

        self._view.update_page()
        return




    def handlePercorso(self, e):
        if self._squadraSelezionata is None:
            self._view._txt_result.clean()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare una squadra!", color="red"))
            self._view.update_page()
            return
        if not self._model.esisteGrafo():
            self._view._txt_result.clean()
            self._view._txt_result.controls.append(ft.Text(f"Creare un grafo!", color="red"))
            self._view.update_page()
            return

        path,score = self._model.getPathV2(self._squadraSelezionata)
        self._view._txt_result.clean()
        self._view._txt_result.controls.append(ft.Text(f"Trovata soluzione lunga {len(path)} con somma pesi archi pari a {score}"))
        for i in range(0,len(path)-1):
            self._view._txt_result.controls.append(ft.Text(f"{path[i]} -> {path[i+1]} con peso: {path[i].salarioTotale + path[i+1].salarioTotale} "))
        self._view.update_page()
        return
    def fillDdAnno(self):
        anni = self._model.getAnni()
        for a in anni:
            self._view._ddAnno.options.append(
                ft.dropdown.Option(key=a,
                                   on_click = self._handleAnnoSelezionato))
        return

    def _handleAnnoSelezionato(self, e):
        self._squadraSelezionata = None
        self._annoSelezionato = e.control.key
        self._model.svuotaGrafo()

        squadreAnno = self._model.getSquadreAnno(self._annoSelezionato)
        self._view._txtOutSquadre.clean()
        self._view._txt_result.clean()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Nell'anno {self._annoSelezionato} hanno giocato {len(squadreAnno)} squadre"))
        for s in squadreAnno:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{s.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=s.teamCode,
                                                                    data=s,
                                                                    on_click = self._handleSquadraSelezionata))
        self._view._ddSquadra.value = None
        self._squadraSelezionata = None
        self._view.update_page()
        return

    def _handleSquadraSelezionata(self, e):
        self._squadraSelezionata = e.control.data
        return