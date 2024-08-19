"""
Created on Wed Feb  7 20:31:26 2024

@author: laurasofiahurtadourrego
"""
#Maria GABRIELA Correa ARguello
#Laura Sofia Hurtado Urrego

from gurobipy import Model,GRB,quicksum
import pandas as pd

#Datos
file_name = 'dd.xlsx'
conjuntos = pd.read_excel(io=file_name, sheet_name="Conjuntos")

# Conjuntos
P = [p for p in conjuntos["Procesos"] if not pd.isna(p)]
E = [e for e in conjuntos["Estaciones"] if not pd.isna(e)]

# Parámetros
d = pd.read_excel(io=file_name, sheet_name="Distancias", index_col=[0, 1]).squeeze()
f = pd.read_excel(io=file_name, sheet_name="Flujos", index_col=[0, 1]).squeeze()

# Modelo de optimizacion
m = Model("Distanciamiento")

# Variables
x = m.addVars(P, E, vtype=GRB.BINARY, name="x")
y = m.addVars(P, E, E,P, vtype=GRB.BINARY, name="y")

# Restricciones
# 1) Que cada estación quede asignada a un proceso
for p in P:
    m.addConstr(quicksum(x[p, e] for e in E) == 2)

# Restricciones para linealizar la función 
for i in P:
    for j in E:
        for s in E:
            for n in P:
                m.addConstr(y[i, j, s,n] >= x[i, j] + x[n, s] - 1)

# Función Objetivo
m.setObjective(quicksum( d[j, s] * f[i, l] * y[i, j, s, l] for i in P for j in E for s in E for l in P), GRB.MINIMIZE)

# Optimizar
m.update()
m.optimize()

# Mostrar valor óptimo
z = m.getObjective().getValue()

# Impresion de resultados
for p, e in x.keys():
    if x[p, e].x > 0:
        print("El proceso ", p, "hay que ubicarlo en la estacion ", e)
