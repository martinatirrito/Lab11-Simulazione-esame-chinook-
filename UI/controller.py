import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGenre()
        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view.update_page()

    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        artists = self._model.getArtists()
        for artist in artists:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=artist.ArtistId,text=artist.Name))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph(self._view._ddGenre.value)
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f'Grafo correttamente creato.'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {Nnodes}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {Nedges}'))

    #MIGLIOR ARTISTA INFLUENTE PESO ARC USCETE - PESO ARC ENTRANTE
        artista, score = self._model.getBestInfluenzaArtista()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {artista}, con influenza: {score}"))

    #TOP 5 ARCHI PESO MAGGIORE DECRS
        top5 = self._model.getTop5Archi()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for a in top5:
            self._view.txt_result.controls.append(ft.Text(f'{a[0]} -> {a[1]} : {a[2]["weight"]}'))

        self.fillDDArtist()


        self._view.update_page()

    def handleCammino(self,e):
        pass