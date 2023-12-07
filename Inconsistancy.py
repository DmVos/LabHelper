from numpy import exp, array, random, dot
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools 
from tkinter import *
from tkinter import ttk
import tkinter as tk
import rdflib
from rdflib import *
import plotly.graph_objects as go
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser
import re
import os

working_dir = os.path.dirname(os.path.abspath(__file__))

g = rdflib.Graph()
result = g.parse(file=open(os.path.join(working_dir, "Rules.n3"), "r"), format="text/n3")

g2 = rdflib.Graph()
result3 = g2.parse(file=open(os.path.join(working_dir, "KB.n3"), "r"), format="text/n3")


Ruleqres = g.query(
            """SELECT DISTINCT ?allofKPIs
               WHERE {
                    ind:KPIs owl:oneOf ?allofKPIs.
               }""")


allofKPIslist=[]
for row in Ruleqres:
    allofKPIs = str(row.asdict()['allofKPIs'].toPython())
    allofKPIslist.append(allofKPIs)


allofKPIslist.sort()

print("========== RULE owl:oneof KPIs =========")
print(allofKPIslist)

# =========================================================

Ruleqres1 = g.query(
            """SELECT DISTINCT ?allofSPs
               WHERE {
                    ind:SubProcesses owl:oneOf ?allofSPs.
               }""")


allofSPslist=[]
for row in Ruleqres1:
    allofSPs = str(row.asdict()['allofSPs'].toPython())
    allofSPslist.append(allofSPs)

allofSPslist.sort()

print("========== RULE owl:oneof SPs =========")
print(allofSPslist)

# =========================================================

Ruleqres2 = g.query(
            """SELECT DISTINCT ?allofResources
               WHERE {
                    ind:Resources owl:oneOf ?allofResources.
               }""")

allofResourceslist=[]
for row in Ruleqres2:
    allofResources = str(row.asdict()['allofResources'].toPython())
    allofResourceslist.append(allofResources)

allofResourceslist.sort()

print("========== RULE owl:oneof Resources =========")
print(allofResourceslist)

# =========================================================

Ruleqres3 = g.query(
            """SELECT DISTINCT ?allofIOs
               WHERE {
                    ind:IOs owl:oneOf ?allofIOs.                    
               }""")

allofIOslist=[]
for row in Ruleqres3:
    allofIOs = str(row.asdict()['allofIOs'].toPython())
    allofIOslist.append(allofIOs)

allofIOslist.sort()

print("========== RULE owl:oneof IOs =========")
print(allofIOslist)

# =========================================================

Ruleqres4 = g.query(
            """SELECT DISTINCT ?allofmembers
               WHERE {
                ?member owl:members ?allofmembers.
               }""")

allofmemberslist=[]
for row in Ruleqres4:
    allofmembers = str(row.asdict()['allofmembers'].toPython())
    allofmemberslist.append(allofmembers)


allofmemberslist.sort()

print("========== RULE owl:members =========")
print(allofmemberslist)

# =========================================================

Ruleqres5 = g.query(
            """SELECT DISTINCT ?propAsymmetric
               WHERE {
                ?propAsymmetric a owl:AsymmetricProperty.
               }""")

propAsymmetriclist=[]
for row in Ruleqres5:
    propAsymmetric = str(row.asdict()['propAsymmetric'].toPython())
    propAsymmetriclist.append(propAsymmetric)


propAsymmetriclist.sort()

print("========== RULE owl:AsymmetricProperty =========")
print(propAsymmetriclist)

# =========================================================

Ruleqres6 = g.query(
            """SELECT DISTINCT ?propIrreflexive
               WHERE {
                ?propIrreflexive a owl:IrreflexiveProperty.
               }""")

propIrreflexivelist=[]
for row in Ruleqres6:
    propIrreflexive = str(row.asdict()['propIrreflexive'].toPython())
    propIrreflexivelist.append(propIrreflexive)


propIrreflexivelist.sort()

print("========== RULE owl:IrreflexivecProperty =========")
print(propIrreflexivelist)

# =========================================================
# =========================================================

KBqres = g2.query(
            """SELECT DISTINCT ?kpi ?ExistingKPIs
               WHERE {
                  ?kpi prop:hasKPI ?ExistingKPIs.
               }""")
kpilist=[]
ExistingKPIslist=[]
for row in KBqres:
    kpi = str(row.asdict()['kpi'].toPython())
    ExistingKPIs = str(row.asdict()['ExistingKPIs'].toPython())
    kpilist.append(kpi)
    ExistingKPIslist.append(ExistingKPIs)


print("========== KB prop:hasKPI =========")
print(kpilist)
print(ExistingKPIslist)

# =========================================================

KBqres1 = g2.query(
            """SELECT DISTINCT ?sp ?ExistingSPs
               WHERE {
                  ?sp prop:hasSubProcess ?ExistingSPs.
               }""")
splist=[]
ExistingSPslist=[]
for row in KBqres1:
    sp = str(row.asdict()['sp'].toPython())
    ExistingSPs = str(row.asdict()['ExistingSPs'].toPython())
    splist.append(sp)
    ExistingSPslist.append(ExistingSPs)


print("========== KB prop:hasSubProcess =========")
print(splist)
print(ExistingSPslist)

# =========================================================

KBqres2 = g2.query(
            """SELECT DISTINCT ?resource ?ExistingResources
               WHERE {
                  ?resource prop:hasResource ?ExistingResources.
               }""")
resourcelist=[]
ExistingResourceslist=[]
for row in KBqres2:
    resource = str(row.asdict()['resource'].toPython())
    ExistingResources = str(row.asdict()['ExistingResources'].toPython())
    resourcelist.append(resource)
    ExistingResourceslist.append(ExistingResources)


print("========== KB prop:hasResource =========")
print(resourcelist)
print(ExistingResourceslist)

# =========================================================

KBqres3 = g2.query(
            """SELECT DISTINCT ?io ?ExistingIOs
               WHERE {
                  ?io prop:hasIO ?ExistingIOs.
               }""")

iolist=[]
ExistingIOslist=[]
for row in KBqres3:
    io = str(row.asdict()['io'].toPython())
    ExistingIOs = str(row.asdict()['ExistingIOs'].toPython())
    iolist.append(io)
    ExistingIOslist.append(ExistingIOs)


print("========== KB prop:hasIO =========")
print(iolist)
print(ExistingIOslist)

# =========================================================

KBqres4 = g2.query(
            """SELECT DISTINCT ?ind
               WHERE {
                  ?ind a ?allofmembers.
                  }""")

indlist=[]

for row in KBqres4:
    ind = str(row.asdict()['ind'].toPython())
    indlist.append(ind)

print("========== KB members of classes =========")
print(indlist)

# =========================================================

KBqres5 = g2.query(
            """SELECT DISTINCT ?indAP1 ?indAP2
               WHERE {
                  ?indAP1 ?propAsymmetric ?indAP2.
                  ?indAP2 ?propAsymmetric ?indAP1.
               }""")

indAP1list=[]
indAP2list=[]
for row in KBqres5:
    indAP1 = str(row.asdict()['indAP1'].toPython())
    indAP2 = str(row.asdict()['indAP2'].toPython())
    indAP1list.append(indAP1)
    indAP2list.append(indAP2)


print("========== KB AsymmetricProperty =========")
print(indAP1list)
print(indAP2list)

# =========================================================

KBqres6 = g2.query(
            """SELECT DISTINCT ?indIP1
               WHERE {
                  ?indIP1 ?propIrreflexive ?indIP1.
                  }""")

indIP1list=[]
indIP2list=[]
for row in KBqres6:
    indIP1 = str(row.asdict()['indIP1'].toPython())
    indIP2 = str(row.asdict()['indIP2'].toPython())
    indIP1list.append(indIP1)
    indIP2list.append(indIP2)


print("========== KB Irreflexive Property =========")
print(indIP1list)
print(indIP2list)

# =========================================================
# =========================================================

for item in ExistingKPIslist:
    if item in allofKPIslist:
        print(item+'    in list')
    else:
        print("Inconsistency Found in item  "+item)

for item in ExistingSPslist:
    if item in allofSPslist:
        print(item+'    in list')
    else:
        print("Inconsistency Found in item  "+item)

for item in ExistingResourceslist:
    if item in allofResourceslist:
        print(item+'    in list')
    else:
        print("Inconsistency Found in item  "+item)

for item in ExistingIOslist:
    if item in allofIOslist:
        print(item+'    in list')
    else:
        print("Inconsistency Found in item  "+item)
        

for item in indlist:
    if indlist.count(item) > 1:
        print("Inconsistency Found in item  "+item)
        break
else:
    print("AllDisjointClasses inconsistency is not found.")   


if (indAP1list == indAP2list) and (indAP1list != []):
       for item in indAP1list:
        print("Inconsistency Found in item  "+item) 
else:
    print("Asymmetric Proprty inconsistency is not found.")


if indIP1list != []:
       for item in indIP1list:
        print("Inconsistency Found in item  "+item) 
else:
    print("IrreflexiveProperty inconsistency is not found.")


