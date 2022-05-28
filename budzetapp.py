# pydoc3 -w ./
# poprawione z zaleceniami PEP8

import gi
from gi.repository import Gtk, GLib
import DataBase

gi.require_version("Gtk", "3.0")


class EntryWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Grid Example")

        # Dodawanie nowej kategorii

        label1 = Gtk.Label(label="Dodaj kategorie")
        
        self.entrycat = Gtk.Entry()
        self.entrycat.set_text("podaj nazwe kategorii")

        self.entrym = Gtk.Entry()
        self.entrym.set_text("podaj miesiac")

        self.entryplan = Gtk.Entry()
        self.entryplan.set_text("podaj planowana kwote")

        self.entryreal = Gtk.Entry()
        self.entryreal.set_text("podaj wydana kwote")

        button1 = Gtk.Button(label="Dodaj kategorie")
        button1.connect("clicked", self.addingCategory)
        
        self.grid = Gtk.Grid()
        self.grid.attach(label1, 1, 0, 2, 1)
        self.grid.attach(self.entrycat, 1, 1, 2, 1)
        self.grid.attach(self.entrym, 1, 2, 2, 1)
        self.grid.attach(self.entryplan, 1, 3, 2, 1)
        self.grid.attach(self.entryreal, 1, 4, 2, 1)
        self.grid.attach_next_to(button1, self.entrycat, 
                                 Gtk.PositionType.RIGHT, 1, 4)

        # Aktualizowanie wydatkow

        label3 = Gtk.Label(label="Dodaj wydatek")

        self.entrymo = Gtk.Entry()
        self.entrymo.set_text("podaj miesiac")

        self.entrychange = Gtk.Entry()
        self.entrychange.set_text("podaj wydana kwote")

        self.entryfindcat = Gtk.Entry()
        self.entryfindcat.set_text("podaj nazwe kategorii")
        
        button2 = Gtk.Button(label="Aktualizuj")
        button2.connect("clicked", self.changeCat)

        self.grid.attach(label3, 1, 5, 2, 1)
        self.grid.attach(self.entryfindcat, 1, 6, 2, 1)
        self.grid.attach(self.entrymo, 1, 7, 2, 1)
        self.grid.attach(self.entrychange, 1, 8, 2, 1)
        self.grid.attach_next_to(button2, self.entryfindcat, 
                                 Gtk.PositionType.RIGHT, 1, 3)

        # Wypisywanie budzetu

        self.odstep2 = Gtk.Label(label="")
        self.grid.attach(self.odstep2, 1, 9, 2, 1)
        
        self.tabela_tytul = Gtk.Label()
        self.tabela_tytul.set_markup("<big>Aktualny budzet</big>")
        self.grid.attach(self.tabela_tytul, 1, 10, 2, 1)
        self.odstep3 = Gtk.Label(label="")
        self.grid.attach(self.odstep3, 1, 11, 2, 1)

        self.liststore = Gtk.ListStore(str, str, str)

        treeview = Gtk.TreeView(model=self.liststore)

        column_cat = Gtk.TreeViewColumn("Kategoria", Gtk.CellRendererText(), 
                                        text=0)
        treeview.append_column(column_cat)

        column_plan = Gtk.TreeViewColumn("Plan", Gtk.CellRendererText(), 
                                         text=1)
        treeview.append_column(column_plan)

        column_real = Gtk.TreeViewColumn("Realia", Gtk.CellRendererText(),
                                         text=2)
        treeview.append_column(column_real)

        self.grid.attach(treeview, 1, 13, 2, 1)

        self.entrymonth = Gtk.Entry()
        self.entrymonth.set_text("podaj miesiac")
        self.grid.attach(self.entrymonth, 1, 12, 2, 1)

        self.button4 = Gtk.Button(label="Wyswietl tabele")
        self.button4.connect("clicked", self.tabelka)
        self.grid.attach_next_to(self.button4, self.entrymonth, 
                                 Gtk.PositionType.RIGHT, 1, 1)

        self.add(self.grid)

        self.set_size_request(300, 400)

        self.timeout_id = None

    # Dodawanie kategorii

    def addingCategory(self, button):
        v1 = self.entrycat.get_text()
        v2 = self.entrym.get_text()
        v3 = self.entryplan.get_text()
        v4 = self.entryreal.get_text()
        DataBase.addCategory(v1, v2, v3, v4)

    # Aktualizacja wydatkow

    def changeCat(self, button):
        v1 = self.entryfindcat.get_text()
        v2 = self.entrymo.get_text()
        v3 = self.entrychange.get_text()
        DataBase.changeCategory(v1, v2, v3)
        tabel = DataBase.sesja.query(DataBase.Budzet
                                     ).filter(DataBase.Budzet.category == v1,
                                              DataBase.Budzet.month == v2)
        for t in tabel:
            arr = str(t).split(",")
        # Okno dialogowe informujace o sumie wydatkow w danej kategorii
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Aktualizacja wydatkow",
        )
        dialog.format_secondary_text(
            "W kategorii " + arr[1] + " na miesiac " + arr[4] + " wydano" + 
            arr[3] + " z " + arr[2]
        )
        dialog.run()
        dialog.destroy()

    # Wypisywanie tabelki

    def tabelka(self, button):
        v1 = self.entrymonth.get_text()
        tabel = DataBase.sesja.query(DataBase.Budzet
                                     ).filter(DataBase.Budzet.month == v1)
        self.liststore.clear()
        for t in tabel:
            arr = str(t).split(",")
            self.liststore.append([arr[1], arr[2], arr[3]])
