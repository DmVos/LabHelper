from tkinter import *
from tkinter import ttk
import tkinter as tk
import rdflib
from rdflib import *
import plotly.graph_objects as go
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import re, os

root = Tk()
root.title("Treeview Structure of LabHelper")
#root.geometry("1200x680+50+20")

# file_location = os.path.dirname(os.path.abspath(__file__))
KB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KB.n3")

g = rdflib.Graph()
result = g.parse(file=open(KB_path, "r"), format="text/n3")


treeview = ttk.Treeview(root)
#text1 = tk.Text(root, height = 20, width = 75)

qres = g.query(
    """SELECT DISTINCT ?label ?class
       WHERE {
          ?class rdf:type classes:Process .
          ?class rdfs:label ?label .
       }""")

for row in qres:
    a = str(row.asdict()['label'].toPython())
    aa = str(row.asdict()['class'].toPython())
    #print("%s is %s" % row)
    print(a)
    print('=======process ind======')
    print(aa)
    parent = treeview.insert('', 'end' ,a, text = a, open = True )

qres2 = g.query(
    """SELECT DISTINCT ?label ?class
       WHERE {
          ?class prop:SubProcess ind:A0 .
          ?class rdfs:label ?label .
       }""")

for row in qres2:
    b = str(row.asdict()['label'].toPython())
    bb = str(row.asdict()['class'].toPython())
    #print("%s is %s" % row)
    print(b)
    print('=====process ind of sub process of A0=====')
    print(bb)
    child1 = treeview.insert(parent,'end',b, text = b, open = True)

proclabel=[a,b]



treeview.config(column = ('Details'))
treeview.config(height = 10)
treeview.column('#0', width = 300)
treeview.column('Details', width = 300)

treeview.heading('#0', text = 'Process Names')
treeview.heading('Details', text = 'Details')

treeview.pack(fill='x')
root.mainloop()
