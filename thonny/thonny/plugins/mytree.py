import logging
import tkinter as tk
from thonny import  get_workbench, ui_utils
from thonny.languages import tr

logger = logging.getLogger(__name__)

class ValueTree(ui_utils.TreeFrame):
    def __init__(self, master):
        ui_utils.TreeFrame.__init__(
            self,
            master,
            columns=("one","two","three"),
            displaycolumns=(0,),
        )

        self.tree.column("#0", width=1000, minwidth=1000, stretch=tk.NO)
        self.tree.heading("#0",text="Variable",anchor=tk.W)
        self.tree["show"] = ("headings", "tree")

        self.maxdepth = 20
        self.globals_vars = None

        self.itemName = []

        get_workbench().bind("Insert_line", self.insert_line2, True)
        get_workbench().bind("Insert_object", self.insert_object, True)
        get_workbench().bind("Fill_global", self.fill_global, True)

    def fill_global(self, event):
        self._clear_tree()
        self.globals_vars = event.myglobal
        self.remove_all_vars()

    #remove the variable all_vars from the globals variables
    def remove_all_vars(self):
        for i in range(0, len(self.globals_vars)-1):
            if(self.globals_vars[i][0] == "all_vars"):
                del(self.globals_vars[i])

    def get_type_str (self, item):
        type_str = type(item).__name__
        if hasattr (item, '__iter__'): # 'equivalent' de if type(item) == list
            type_str += f': {len(item)}'
        type_str = '{'+type_str+'}'
        return type_str


    def insert_line2(self, event):
        self.insert_line(event.parent_id, event.item, event.item_name, 0, 100)


    def insert_line (self, parent_id, item, item_name, depth, max_depth):
        item_str = f'{item_name} = {str(item)}'

        # ne pas rajouter dans l'arbre si déjà présent
        self.itemName.append(item_name)
        id = self.tree.insert(parent_id, 'end', text=item_str)
        if hasattr (item, '__iter__') and depth <= self.maxdepth:
            for i,elt in enumerate(item):
                self.insert_line (id, elt, i, depth+1, max_depth)

    def isin_globals(self, item):
        for elem in self.globals_vars:
            if(len(elem) == 3 and elem[1] == item):
                return elem
        return None

    def isInTree(self, item):
        for record in self.tree.get_children():
            if(record == item):
                return True

    def insert_object(self, event):
        self.insert_object2(event.parent_id, event.item, event.item_name, 0, 100)

    def insert_object2(self, parent_id, item, item_name, depth, max_depth):
        if len(item) == 0:
            return
        item_str = f'{item_name}'

        if(self.isInTree(item_name)):
            pass
        else:
            id = self.tree.insert(parent_id, 'end',item_name, text=item_str)

            for i in range(len(item)):
                elem = item[i]
                if(len(elem) == 2):
                    self.insert_object2(id, str(elem[1]), str(elem[1]), depth+1, max_depth)


def load_plugin() -> None:
    get_workbench().add_view(ValueTree, tr("Values tree"), "ne")
