import gi
import threading

from model import Model
from view import View


class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_view(self):
        self.view.connect_searchBtn_clicked(self.on_search_button_clicked)
        self.view.connect_searchBtn2_clicked(self.on_search_button2_clicked)
        self.view.connect_select(self.on_user_tree_selection_changed)

    def run(self):
        self.view.run()

    def dialog(self, str):
        self.view.dialog_label.set_label(str)
        self.view.dialog.show_all()
        self.view.dialog.run()
        self.view.dialog.hide()

    def on_search_button_clicked(self, widget):
        text = self.view.entryName.get_text()
        self.view.text2 = text.split()

        try:
            data = self.model.search_user_data(self.view.text2)

        except:
            self.dialog("Error")

        if (data['users'] == []):
            self.dialog("Usuario no encontrado")
        self.view.append_user_data(data)


    def on_search_button2_clicked(self, widget):
        try:
            name = self.view.entryName2.get_text()
            self.view.text3 = name.split()
            name_data = self.model.search_user_data(self.view.text3)
            uuid = name_data['users'][0]['uuid']
            date = self.view.entryDate.get_text()
            array_ids = self.model.search_tracker_data2(uuid, date)
            for x in range(len(array_ids)):
                nombre = self.model.search_tracker_data(array_ids[x], date)
                self.view.append_tracker_data(nombre)
        except:
            self.dialog("Error")


    def on_user_tree_selection_changed(self, selection):
        data = self.model.search_user_data(self.view.text2)
        self.view.qr(data, selection)

