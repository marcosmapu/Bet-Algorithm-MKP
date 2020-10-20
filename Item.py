import random
from importtest import bagsNumber, listaJog, dados, itemsNumber
import copy
from scipy import linalg as LA
class Item:
    def __init__(self, name: str, profit: float, weight:list):
        self.name = name
        self.profit = profit
        self.weight = weight
    
"""items_List = [Item("aa",118,[821, 0.8]), Item("ab", 322,[1144, 1]), Item("ac", 166,[634, 0.7]), Item("ad",195, [701, 0.9]),
        Item("ae",100,[291, 0.9]), Item("af",142,[1702, 0.8]), Item("ag",100,[1633, 0.7]), Item("ah",145,[1086, 0.6]),
        Item("ai",100,[124, 0.6]), Item("aj",208,[718, 0.9]), Item("ak",100,[976, 0.6]), Item("al",312,[1438, 0.7]),
        Item("am",198,[910, 1]), Item("an",171,[148, 0.7]), Item("ao",117,[1636, 0.9]), Item("ap",100,[237, 0.6]),
        Item("aq",329,[771, 0.9]), Item("ar",391,[604, 0.6]), Item("as",100,[1078, 0.6]), Item("at",120,[640, 0.8]),
        Item("au",188,[1510, 1]), Item("av",271,[741, 0.6]), Item("aw",334,[1358, 0.9]), Item("ax",153,[1682, 0.7]),
        Item("ay",130,[993, 0.7]), Item("az",100,[99, 0.7]), Item("ba",154,[1068, 0.8]), Item("bb",289,[1669, 1])]"""
items_List = []

for i in range(itemsNumber): #y[1] = numero de itens
    #a = 2 + itemsNumber + bagsNumber + i*bagsNumber
    #b = 2 + itemsNumber + bagsNumber + (i+1)*bagsNumber
    constraint = []
    for k in range(bagsNumber):
            constraint.append(dados[3+(k+1)*itemsNumber+i])
    items_List.append(Item('Item-'+str(i),dados[3+i],constraint))
items_weight = []
#print("tamanho", len(items_List))
for i in range(len(items_List)):
    weight_List = []
    for _ in range(bagsNumber):
        #weight_List.append(random.randint(1,7))
        items_weight.append([])
    #items_List.append(Item('Item-'+str(i), random.randint(1,15), copy.deepcopy(weight_List)))

"""
items_List.append(Item("Geladeira Dako", 999.90, 0.751))
items_List.append(Item("Iphone 6", 2911.12, 0.0000899))
items_List.append(Item("TV 55' ", 4346.99, 0.400))
items_List.append(Item("TV 50' ", 3999.90, 0.290))
items_List.append(Item("TV 42' ", 2999.00, 0.200))
items_List.append(Item("Notebook Dell", 2499.90, 0.00350))
items_List.append(Item("Ventilador Panasonic", 199.90, 0.496))
items_List.append(Item("Microondas Electrolux", 308.66, 0.0424))
items_List.append(Item("Microondas Panasonic", 299.29, 0.0319))
items_List.append(Item("Microondas LG", 429.90, 0.0544))
items_List.append(Item("Geladeira Brastemp", 849.00, 0.635))
items_List.append(Item("Geladeira Consul", 1199.89, 0.870))
items_List.append(Item("Notebook Lenovo", 1999.90, 0.498))
items_List.append(Item("Notebook Asus", 3999.00, 0.527))
"""
items_name = []
items_profit = []


# Sorting the Item list 

items_List = sorted(items_List, key = lambda i: i.profit, reverse = False)
totalWeight = 0
itemsProb1 = []
for i in items_List:
    items_name.append(i.name)
    items_profit.append(i.profit)
    totalWeight += LA.norm(i.weight)
x = 0
for i in items_List:
        x += LA.norm(i.weight)/totalWeight
        itemsProb1.append(x)
for i in range(bagsNumber):
    for item in items_List:
        items_weight[i].append(item.weight[i])
