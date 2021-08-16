import tkinter as tk
from tkinter import messagebox

import thonny
from graphviz import Digraph
from tkdocviewer import DocViewer
from thonny import get_workbench, tktextext, ui_utils
from thonny.debugger import AssistantRstText
from thonny.languages import tr
from thonny.ui_utils import scrollbar_style
from tkinter import *

class GraphView(tktextext.TextFrame):
    def __init__(self, master):
        tktextext.TextFrame.__init__(
            self,
            master,
            text_class=AssistantRstText,
            vertical_scrollbar_style=scrollbar_style("Vertical"),
            horizontal_scrollbar_style=scrollbar_style("Horizontal"),
            horizontal_scrollbar_class=ui_utils.AutoScrollbar,
            read_only=True,
            wrap="word",
            font="TkDefaultFont",
            padx=10,
            pady=0,
            insertwidth=0,
        )

        self.label = "{"

        newWindow = Toplevel(master)
        newWindow.title("New Window")
        newWindow.geometry("900x700")

        self.v = DocViewer(newWindow)
        self.myGraph = Digraph(comment='My Graph', strict=True)
        self.create_file()
        self.create_and_render()

        self.myVar = None
        get_workbench().bind("Fill_myVar", self.fill_myVar, True)

        get_workbench().bind("Open_GraphViz_with_tab", self.show_list, True)
        get_workbench().bind("Open_GraphViz_with_dict", self.show_dict, True)
        get_workbench().bind("Open_GraphViz_with_object", self.show_object, True)

    def fill_myVar(self, event):
        self.myVar = event.var

    def create_and_render(self):
        self.v.pack(side="top", expand=1, fill="both")
        self.v.display_file("Graph.pdf")

    def create_file(self):
        self.myGraph.render('/Users/damien/Downloads/thonny/thonny/Graph')
        self.create_and_render()

    def parcour_var(self, id):
        for elem in self.myVar:
            if elem[1] == id:
                return elem
        return None

    def has_edge(self, v1, v2):
        tail_name = self.myGraph._quote_edge(v1)
        head_name = self.myGraph._quote_edge(v2)
        return (self.myGraph._edge % (tail_name, head_name, '')) in self.myGraph.body


    def show_list(self, event):
        self.myGraph = Digraph(comment='My Graph', strict=True)
        list_id = event.id
        mylist = event.element
        list_name = event.name

        if(list_name != None):
            self.myGraph.node(str(list_id), str(list_name[0]))
            self.myGraph.node(str(list_name[2]), label=self.label, shape="record")
        else:
            self.myGraph.node(list_id, str(list_name[2]))
            self.myGraph.node(str(list_name[2]), label=self.label, shape="record")

        for i in range(0,len(mylist)):
            elem = mylist[i]
            if type(elem) == list or type(elem) == tuple or type(elem) == set:
                nodeName = str(list_id) + "_" + str(i)
                s = "<" + str(nodeName) + "> " + " | "
                self.label += s
                ref = str(list_name[2]) + ":" + str(nodeName)
                #self.myGraph.node(str(elem), shape="record")
                self.create_node_list(str(elem),elem)
                self.myGraph.edge(str(ref), str(elem))

            # TODO
            elif type(elem) == dict:
                nodeName = str(list_id) + "_" + str(i)
                s = "<" + str(nodeName) + "> " + " | "
                self.label += s
                ref = str(list_name[2]) + ":" + str(nodeName)
                self.myGraph.node(str(elem), shape="record")
                self.myGraph.edge(str(ref), str(elem))
                self.create_node_dict(str(elem), elem)

            elif type(elem) == str and "0x" in elem:
                nodeName = str(list_id) + "_" + str(i)
                s = "<" + str(nodeName) + "> " + " | "
                self.label += s
                ref = str(list_name[2]) + ":" + str(nodeName)
                self.myGraph.node(str(elem))
                self.myGraph.node(str(elem) + "_attr", label="None", shape="record")
                self.myGraph.edge(str(elem), str(elem) + "_attr")
                self.myGraph.edge(str(ref), str(elem) + "_attr")

            else:
                s = str(elem) + " | "
                self.label += s

        self.label = self.label[:-2]
        self.label += "}"
        self.myGraph.edge(str(list_id), str(list_name[2]))
        self.myGraph.node(str(list_name[2]), label=self.label, shape="record")
        self.label = "{"
        self.create_file()


    def create_node_list(self, ref, mylist):
        mylabel = "{"
        i = 0
        for elem in mylist:
            if type(elem) == list or type(elem) == tuple or type(elem) == set:
                nodeName = str(mylist) + "_" + str(i)
                s = "<" + str(nodeName) + "> " + " " +  " | "
                mylabel += s
                #ref = str(mylist) + ":" + str(nodeName)
                self.myGraph.node(str(elem), shape="record")
                self.myGraph.edge(str(ref), str(elem))
                self.create_node_list(str(elem),elem)
            else:
                s = str(elem) + " | "
                mylabel += s
            i += 1

        mylabel = mylabel[:-2]
        mylabel += "}"
        self.myGraph.node(str(mylist), label=mylabel, shape="record")


    def show_dict(self, event):
        # a voir si je garde de refaire tout le dessin
        self.myGraph = Digraph(comment='My Graph', strict=True)
        dict_id = event.id
        mydict = event.entries
        dict_name = event.name

        if (dict_name != None):
            self.myGraph.node(str(dict_id), str(dict_name[0]))
            self.myGraph.node(str(dict_name[2]), label=self.label, shape="record")
        else:
            self.myGraph.node(dict_id, str(dict_name[2]))
            self.myGraph.node(str(dict_name[2]), label=self.label, shape="record")

        for name, val in mydict.items():
            if type(val) == list or type(val) == tuple or type(val) == set:
                nodeName = str(dict_id) + "_" + str(val)
                s = "<" + str(nodeName) + "> " + str(name) + " ; " + " | "
                self.label += s
                ref = str(dict_name[2]) + ":" + str(nodeName)
                self.myGraph.node(str(val), shape="record")
                self.myGraph.edge(str(ref), str(val))
                self.create_node_list(str(val), val)


            elif type(val) == str and "0x" in val:
                nodeName = str(dict_id) + "_" + str(val)
                s = "<" + str(nodeName) + "> " + str(name) + " ; " + " | "
                self.label += s
                ref = str(dict_name[2]) + ":" + str(nodeName)
                self.myGraph.node(str(val))
                self.myGraph.node(str(val) + "_attr", label="None", shape="record")
                self.myGraph.edge(str(val), str(val) + "_attr")
                self.myGraph.edge(str(ref), str(val) + "_attr")

            else:
                s = str(name) + " ; " + str(val) + " | "
                self.label += s

        self.label = self.label[:-2]
        self.label += "}"
        self.myGraph.edge(str(dict_id), str(dict_name[2]))
        self.myGraph.node(str(dict_name[2]), label=self.label, shape="record")
        self.label = "{"
        self.create_file()


    def create_node_dict(self, ref, mydict):
        mylabel = "{"
        for name, val in mydict.items():
            if type(val) == list or type(val) == tuple or type(val) == set:
                nodeName = str(mydict) + "_" + str(val)
                s = "<" + str(nodeName) + "> " + str(name) + " ; " + " | "
                mylabel += s
                ref = str(mydict) + ":" + str(nodeName)
                self.myGraph.node(str(val), shape="record")
                self.myGraph.edge(str(ref), str(val))
                self.create_node_list(str(val), val)

            elif type(val) == dict:
                # TODO
                return
            else:
                s = str(name) + " ; " + str(val) + " | "
                mylabel += s

        mylabel = mylabel[:-2]
        mylabel += "}"
        self.myGraph.node(str(mydict), label=mylabel, shape="record")


    # event.name = (node_name if exists, id, addr)
    def show_object(self, event):
        addr = None
        if(event.name != None):
            addr = event.name[2]
            self.myGraph.node(str(addr), label=event.name[0])
        else:
            addr = thonny.memory.format_object_id(event.id)
            self.myGraph.node(str(addr), label=addr)

        if len(event.attributes) != 0:
            mylabel = "{"
            for elem in event.attributes:
                nodeName = str(addr) + "_" + str(elem[0])
                s = "<" + str(nodeName) + "> " + str(elem[0]) + " | "
                mylabel += s
            mylabel = mylabel[:-2]
            mylabel += "}"
            refNode = str(addr) + "_attr"
            self.myGraph.node(refNode, label=mylabel, shape="record")
            self.myGraph.edge(str(addr), refNode)
            self.create_attributes_node(str(addr), event.attributes)

        self.create_file()


    def create_attributes_node(self, addr, attr):

        for elem in attr:
            ref = str(addr) + "_attr" + ":" + str(addr) + "_" + str(elem[0])
            myelem = eval(elem[1])
            if type(myelem) == list or type(myelem) == set or type(myelem) == tuple:
                self.create_node_list(ref,myelem)
                self.myGraph.edge(ref, elem[1])

            # TODO
            elif type(myelem) == dict:
                pass

            elif type(elem[1]) == str and "0x" in elem[1]:
                self.myGraph.node(str(elem[1]), str(elem[1]))
                self.myGraph.node(str(elem[1]) + "_attr", label="None", shape="record")
                self.myGraph.edge(str(addr) + "_attr", str(elem[1] + "_attr"))
                self.myGraph.edge(str(elem[1]), str(elem[1] + "_attr"))
                self.create_file()

            else: # pour les int, float, bool, str
                self.myGraph.node(str(myelem), label=str(myelem), shape="record")
                self.myGraph.edge(ref, str(myelem))
                self.create_file()


def load_plugin() -> None:
    get_workbench().add_view(GraphView, tr("GraphView"), "e")
