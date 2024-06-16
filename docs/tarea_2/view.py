import gi
import threading
import requests
import qrcode
import uuid

gi.require_version("Gtk", "3.0")
from typing import Protocol, Union
from gi.repository import Gtk, GLib, GdkPixbuf
from datetime import datetime,timedelta

class View():

    def __init__(self):

        win = Gtk.Window()
        win.connect("destroy", Gtk.main_quit)
        win.set_title("Aplicacion Covid-19")
        win.set_default_size(830, 650)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_border_width(10)

        grid2 = Gtk.Grid()
        grid2.set_row_spacing(10)
        grid2.set_border_width(10)

        notebook = Gtk.Notebook()
        win.add(notebook)


        #tab1
        insertName = Gtk.Label(label = "Nombre y apellidos")
        entryName = Gtk.Entry()
        searchBtn = Gtk.Button(label = "Buscar")
        searchBtn.set_size_request(80, 30)

        name_box = Gtk.Box()
        name_box.pack_start(insertName, True, True, 0)
        name_box.pack_start(entryName, True, True, 10)
        name_box.pack_start(searchBtn, True, True, 5)

        pageLabel1 = Gtk.Label()
        pageLabel1.set_markup('<b>Localizador</b>')
        notebook.append_page(grid, pageLabel1)

        user_store = Gtk.ListStore(str)
        user_tree = Gtk.TreeView()
        user_tree.set_model(user_store)
        user_rendererText = Gtk.CellRendererText()
        user_column = Gtk.TreeViewColumn("Resultados de la busqueda", user_rendererText, text=0)
        scrollable_user_tree = Gtk.ScrolledWindow()
        scrollable_user_tree.add(user_tree)
        scrollable_user_tree.set_max_content_height(55)
        scrollable_user_tree.set_min_content_height(50)
       
        select = user_tree.get_selection()
       
        image = Gtk.Image()
        imageBox = Gtk.VBox()
        imageBox.add(image)

        user_data_box = Gtk.VBox(spacing = 10)
        username_label = Gtk.Label()
        email_label = Gtk.Label()
        phone_label = Gtk.Label()
        vaccinated_label = Gtk.Label()

        user_data_box.add(username_label)
        user_data_box.add(email_label)
        user_data_box.add(phone_label)
        user_data_box.add(vaccinated_label)

        grid.attach(name_box, 0, 0, 1, 1)
        grid.attach(scrollable_user_tree,0,1,15,5)
        grid.attach_next_to(imageBox,scrollable_user_tree, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(user_data_box,imageBox, Gtk.PositionType.BOTTOM, 1, 1)
        
        #tab2
        insertName2 = Gtk.Label(label = "Nombre y apellidos")
        entryName2 = Gtk.Entry()
        searchBtn2 = Gtk.Button(label = "Buscar")
        searchBtn.set_size_request(80, 30)
        
        name_box2 = Gtk.Box()
        name_box2.pack_start(insertName2, True, True, 0)
        name_box2.pack_start(entryName2, True, True, 10)
        name_box2.pack_start(searchBtn2, True, True, 5)

        grid2.set_border_width(10)
        pageLabel2 = Gtk.Label()
        pageLabel2.set_markup('<b>Rastreador Covid-19</b>')
        notebook.append_page(grid2, pageLabel2)
        grid2.attach(name_box2,0,0,1,1)
        
        insertDate = Gtk.Label(label = "Fecha")
        entryDate = Gtk.Entry()
        entryDate.set_placeholder_text("DD/MM/AAAA")
        
        dateBox = Gtk.Box()
        dateBox.pack_start(insertDate,True, True, 0)
        dateBox.pack_start(entryDate,True, True, 0)
        grid2.attach(dateBox,0,1,1,1)
           
        tracker_store = Gtk.ListStore(str)
        tracker_tree = Gtk.TreeView()
        tracker_tree.set_model(tracker_store)
        tracker_rendererText = Gtk.CellRendererText()
        tracker_column = Gtk.TreeViewColumn("Resultados de la busqueda", tracker_rendererText, text=0)
        scrollable_tracker_tree = Gtk.ScrolledWindow()
        scrollable_tracker_tree.add(tracker_tree)
        scrollable_tracker_tree.set_max_content_height(55)
        scrollable_tracker_tree.set_min_content_height(50)
        grid2.attach_next_to(scrollable_tracker_tree,dateBox,Gtk.PositionType.BOTTOM, 40, 40)

        #dialog
        dialog = Gtk.Dialog(title="Error")
        dialog.set_default_size(300,50) 
        dialog_label = Gtk.Label()
        dialog_box = dialog.get_content_area()
        dialog_box.set_homogeneous(True)
        dialog_box.add(dialog_label)


        #variables
        self.searchBtn = searchBtn
        self.searchBtn2 = searchBtn2
        self.win = win
        self.grid = grid
        self.user_store = user_store
        self.user_tree = user_tree
        self.user_column = user_column
        
        self.tracker_store = tracker_store
        self.tracker_tree = tracker_tree
        self.tracker_column = tracker_column
        
        
        self.tracker_tree = tracker_tree
        self.tracker_store = tracker_store
        
        self.entryName = entryName
        self.entryName2 = entryName2
        self.entryDate = entryDate
        
        self.image = image
        self.imageBox = imageBox
        self.user_data_box = user_data_box
        self.username_label = username_label
        self.email_label = email_label
        self.phone_label = phone_label
        self.vaccinated_label = vaccinated_label
        
        self.dialog = dialog
        self.select = select
        self.dialog_label = dialog_label


    def append_user_data(self, data):
        self.user_store.clear()
        self.win.show_all()
        for x in range(len(data['users'])):
            str1 = ""
            name = ([data['users'][x]['name']])
            surname = ([data['users'][x]['surname']])
            name_surname = name + surname
            for ele in name_surname:
                str1 += " " + ele
            self.user_store.append([str1])
        self.user_tree.append_column(self.user_column)
        self.win.show_all()


    def append_tracker_data(self,data):
        self.tracker_store.clear()    
        name = ""
        name1 = ""
        name2 = "" 
        hist = []   
        for x in range(len(data['access_log'])):            
                name1 = (data['access_log'][x]['user']['name'])
                name2 = (data['access_log'][x]['user']['surname'])
                name = name1+" "+name2 
                cnt=0
                for y in range(len(hist)):                   
                    if(hist[y] != name):
                        cnt = cnt+1
                if (cnt == len(hist)):
                    hist.append(name)                
                    self.tracker_store.append([name])             
                self.tracker_tree.append_column(self.tracker_column)


    def run(self):
        self.win.show_all()
        Gtk.main()

    def stop(self):
        Gtk.main_quit()
                
    def connect_searchBtn_clicked(self, fun):
        self.searchBtn.connect("clicked",fun)
    
    def connect_searchBtn2_clicked(self, fun):
        self.searchBtn2.connect("clicked",fun)
        
    def connect_select(self, fun):
        self.select.connect("changed", fun)
        
    
    def qr(self,data,selection): 
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            index = self.user_tree.get_selection().get_selected_rows()[1][0][0]
            code = data['users'][index]['uuid']
            qrImgGrayscale = qrcode.make(data['users'][index]['name']+ "_" +data['users'][index]['surname']+"_" +str(code))
            qrImg = qrImgGrayscale.convert('RGB')

            b = GLib.Bytes(qrImg.tobytes())
            dkpixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                b,
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                qrImg.size[0],
                qrImg.size[1],
                qrImg.size[0] * (len(qrImg.getbands()))
            )

            if(data['users'][index]['is_vaccinated']):
                vac = "Vacunado"
            else:
                vac = "No vacunado"

            self.username_label.set_label(data['users'][index]['username'])
            self.email_label.set_label(data['users'][index]['email'])
            self.phone_label.set_label(data['users'][index]['phone'])
            self.vaccinated_label.set_label(vac)
            self.image.set_from_pixbuf(dkpixbuf)


