import random
from itertools import chain, combinations
import copy
import House
from Item import items_List, items_weight, itemsProb1
import Knapsack
from operator import add, sub
from importtest import bagsNumber
import time
class Player:
    def __init__(self, knowledge=[], ratings=[], cacife=1000):
        self.knowledge = knowledge
        self.ratings = ratings
        self.cacife = cacife


    def createKnowledge(self, size):
        knowledge = []
        for _ in range(size):
            knowledge.append(random.random())
        self.knowledge = knowledge
        return self.knowledge


    def powerset(self, iterable):        
        s = list(iterable)
        # powerset([1,2,3]) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    

    def createRatings(self, mask: list):
        # ratingSize = 2**len(mask)
        maskSubsets = self.powerset(mask)
        ratings = []  


        #  M = {1,3}
        # T0 = (1 - k[1])*(1 - k[3])
        # T1 = k[1] * (1 - k[3])
        # T2 = k[3] * (1 - k[1])
        # T3 = k[3] * k[1]
       

        for ms in maskSubsets:
            t0,tx = 1,1
            if len(ms) == 0:
                for m in mask:
                    t0 *= (1-self.knowledge[m]) 
                ratings.append(t0)
                # print(t0)            
            else:
                used = []
                # multiply part1 - used
                for i in range(len(ms)):
                    tx *= self.knowledge[ms[i]]
                    used.append(ms[i])
                # print("used", used)
                
                # Getting the diff beteween the lists as sets
                notUsed = list(set(mask)-set(used))
                # print(notUsed)

                # multiply part2 - notUsed
                for i in notUsed:
                    tx *= (1 - self.knowledge[i])
                ratings.append(tx)

        self.ratings = ratings
        # self.ratesSum = sum(self.ratings)
        return self.ratings


    def reset(self):
        self.knowledge = []
        self.ratings = []
        self.cacife = 1000

    def kellyAlgo(self, rating:float, houseProb:float):
        # Kelly = (p*o - 1) / (o - 1)
        # where
        # p = the probability of success, according to player
        # o = howse odd = 1/houseProbs[pick]
        p = rating        
        o = 1/houseProb #HouseProb
        po = p*o
        kelly = ( po - 1.0) / (o - 1.0)
        # print("KELLY:", kelly)
        return kelly
    

    def bet(self, best_so_far: list, House: House, bags_List: list, dictbet, bestWeight, bestProfit, minBet = 15.0, maxBet = 200): #antes: bag:knapsack     
        bets = []
        chosenToBet = []
        risk_list = []
        bestSolprofit = float(bestProfit)
        bestSolWeight = bestWeight[:]
        candidateBet = best_so_far[:]
        chosenToBetIndex = 0 #>>>>>>NEED TO TEST <<<<
        
        for i in range(len(self.ratings)): ###DECIDE ONDE APOSTAR E RISCO TOMADO
            #candidateBet = copy.deepcopy(best_so_far)
            # check if the player has cacife to bet
            if self.cacife > minBet:
                
                # check whether rating is higher than the houseProb
                if self.ratings[i] > House.houseProbs[i]:
                    kelly = self.kellyAlgo(self.ratings[i], House.houseProbs[i])
                    toBet = kelly * self.cacife
                    
                    if toBet < minBet:
                        risk = minBet
                    elif toBet > maxBet:
                        risk = maxBet
                    else:
                        risk = toBet
                    
                    #print(risk)
                    risk_list.append(float(risk))
                    # Only bet if it has enough cacife
                   
                    chosenToBet.insert(i,1)                    
                else:
                    chosenToBet.insert(i,0)
                    risk_list.append(0)
            else:
                chosenToBet.insert(i,0)
                risk_list.append(0)

        # Check if the new solution is valid
        # print("INICIA TESTE###############")
        # print(chosenToBet)
        
        # print(bag.capacity)
        maskSubsets = self.powerset(House.mask)
        
        for y in range(len(chosenToBet)):  ####EXECUTA APOSTA
            if y in dictbet: ### CHECA SE APOSTA JA EXISTE NO DICIONARIO
                dictbet[y][1] = risk_list[y]
                bets.append(dictbet[y])
                
            else:
                if chosenToBet[y] == 1: ### VERIFICA CADA APOSTA
                    weightSum = bestWeight[:]
                    Profit = float(bestProfit)
                    candidateBet = best_so_far[:]
                    for item in maskSubsets[y]:
                        #print("ITEM:", item)
                        # print("I:", i)
                        if candidateBet[item] == 0: ### COLOCA ITEM NA MOCHILA
                            candidateBet[item] = 1 #- candidateBet[item]
                            weightSum = list(map(add,weightSum,items_List[item].weight))
                            Profit += items_List[item].profit
                   
                    ### CRIA LISTA DE ITENS A SEREM REMOVIDOS
                    greedyRemovalList = list(filter(lambda x: x not in maskSubsets[y] and candidateBet[x] == 1, range(len(items_List))))
                           
                    random.shuffle(greedyRemovalList) ###RADOMIZA ESSA LISTA
                    for item in greedyRemovalList:         ###REMOVE OS ITENS    # weightSum, Capacity
                        k = 0
                        for i in range(len(weightSum)):
                            if weightSum[i] > bags_List[i].capacity:
                                if candidateBet[item] == 1:
                                    #print(candidateBet)
                                    #print("remove %i" %item)
                                    candidateBet[item] = 0
                                    #print(candidateBet)
                                    #weightSum[i] -= items_List[item].weight[i]
                                    weightSum = list(map(sub,weightSum,items_List[item].weight))
                                    Profit -= items_List[item].profit
                                    break
                        for i in range(len(weightSum)):
                            if weightSum[i] < bags_List[i].capacity:
                                k += 1
                        if k == len(weightSum):
                            break
                    k = -1
                    """if weightSum[0] > 5000 or weightSum[1] > 5000 or weightSum[2] > 5000 or weightSum[3] > 5000 or weightSum[4] > 5000:
                        print("ESTOUROU")"""
                    for p in items_List: ###ADICIONA NOVOS ITENS GULOSAMENTE
                        counter = 0
                        for i in range(len(weightSum)):
                            if (bags_List[i].capacity - weightSum[i]) >= items_List[k].weight[i]:    
                                counter += 1
                                if candidateBet[k] == 0 and counter == len(weightSum):
                                    #print(candidateBet)
                                    #addIndex = k + len(items_List)
                                    #print("adicionou %i" %addIndex)
                                    candidateBet[k] = 1
                                    #print(candidateBet)
                                    #weightSum[i] += items_List[k].weight[i]
                                    t0 = time.time()
                                    j=0
                                    
                                    weightSum = list(map(add,weightSum,items_List[k].weight))
                                    t1 = time.time()
                                    #print(t1-t0)
                                    Profit += items_List[k].profit
                                    #print(weightSum)
                                    #addIndex = len(items_List) + k
                        k -= 1 
                    betx = candidateBet[:] ## betx = APOSTA
                    #print("terminou de adicionar gulosamente")
                    #print("weightSum: ", weightSum)
                    #print("Profit: ", House.profit(betx))
                    #print("candidateBet: ", betx)
                    #falta colocar detalhes de cada aposta separada nessa identação
                    bets.append([betx, risk_list[y], y, weightSum[:], float(Profit)]) ### LISTA DE APOSTAS
                    #print("BETSX: ", bets)
                #print("hmm",t6-t5)
        #print("bets:", bets)
        finalrisk = 0
        for item in bets: ##VERIFICA QUAL A MELHOR APOSTA
            
            #print("bestSolprofit:", bestSolprofit)
            #print("House.profit(item[0]):",House.profit(item[0]))
            if item[-1] > bestSolprofit:                
                bestSolprofit = item[4]
                bestSolWeight = item[3]
                candidateBet = item[0]
                finalrisk = item[1]
                #print("risk: ",risk)
                chosenToBetIndex = item[2]
        self.cacife -= finalrisk
        
        finalBet = [candidateBet, finalrisk, chosenToBetIndex, bestSolprofit, bestSolWeight, bets]
        #print("finalbet:" ,finalBet)
        #print("aa")
        
        return finalBet

