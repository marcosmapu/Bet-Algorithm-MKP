from Item import items_weight, items_List
import random
#from constants import tightnessFactor

class Knapsack:
    def __init__(self, bagNumber: int, capacity = 3):
        self.capacity = capacity
        self.bagNumber = bagNumber
        
    def setCapacity(self, tightnessFactor: float): #NAO ESTA SENDO USADA PARA OR LIBRARY
        capacity = 0
        for i in items_List:
            capacity += i.weight[self.bagNumber]
        capacity *= tightnessFactor
        self.capacity = capacity

def firstGreedyChoice(cap: float):
    bag = Knapsack(0)
    weightSum = 0
    i = 0
    maxSize = len(items_List)
    choice = []
    while weightSum < sum(items_weight[0]):
        weightSum += items_weight[0][i]        
        #bag.setCapacity(tightnessFactor) #SETA CAPACIDADE
        if weightSum > bag.capacity:
            break
        choice.append(1)
        i += 1

    while maxSize > len(choice):
        choice.append(0)

    return items_weight[0][:i], items_List[:i], choice



        
        
