import csv
import matplotlib.pyplot as plt
import numpy
import random
import sys

x = []
dados = []
datafile = sys.argv[1] #"OR5x100-0.25_1" #sys.argv[1]
with open(str(datafile)+".dat") as csvfile:
    data = csv.reader(csvfile, delimiter= ' ')
    for i in data:
        x += i
for i in x:    
    if i.replace('.','',1).isdigit():
        dados.append(float(i))
#print(dados)
listaJog = []
bagsNumber = int(dados[1])
itemsNumber = int(dados[0])
bagsCapacities = []
"""for i in range(bagsNumber):
    bagsCapacities.append(dados[2 + itemsNumber + i]) #modo problemas padrao
optimal = dados[-1]"""
for i in range(bagsNumber):
    bagsCapacities.append(dados[-bagsNumber+i]) #modo problema novo
optimal = dados[2]
#bagsCapacities = [5000,5000,5000,5000,5000]
