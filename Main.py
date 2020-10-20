import matplotlib.pyplot as plt
from House import House
from Item import Item, items_List, items_name, items_profit, items_weight
from Knapsack import Knapsack
from Player import Player
import random
from importtest import bagsNumber, bagsCapacities, optimal, datafile
import time
import copy
from operator import add, sub
from statistics import mean
import sys
import logging
from logger import resultados_logger, progresso_logger, resultados_1fase_logger, progresso_1fase_logger, output_andre_logger
import datetime

#logging.basicConfig(filename="resultados_"+str(sys.argv[1])+".log", level=logging.INFO, format='%(message)s')
resultados1 = []
resultados2 = []
totaltimes = []
resultados1_1fase = []
resultados2_1fase = []
totaltimes_1fase = []
datafile = sys.argv[1]
print("Comecou problema ", datafile)
now = datetime.datetime.now()
#progresso_logger.info("Problema %s\t\t\t%d/%d/%d\t%d:%d:%d\n" %(sys.argv[1], now.day, now.month, now.year, now.hour, now.minute, now.second))
#progresso_1fase_logger.info("Problema %s\t\t\t%d/%d/%d\t%d:%d:%d\n" %(sys.argv[1], now.day, now.month, now.year, now.hour, now.minute, now.second))
#resultados_logger.info("Problema %s\t\t\t%d/%d/%d\t%d:%d:%d\n" %(sys.argv[1], now.day, now.month, now.year, now.hour, now.minute, now.second))
#resultados_1fase_logger.info("Problema %s\t\t\t%d/%d/%d\t%d:%d:%d\n" %(sys.argv[1], now.day, now.month, now.year, now.hour, now.minute, now.second))
output_andre_logger.info("%s\t%d rounds (1st phase)\toptmal: %d\n\nbest\tgreedy\t1st\t2nd\ttime(s)" %(sys.argv[1], int(sys.argv[2]), optimal))
for run in range(int(sys.argv[3])): #int(sys.argv[3]) ###NUMERO DE VEZES QUE O CODIGO RODA
    

    start = time.time()

    bags_List = []
    # print("peso",items_List[3].weight[2])
    for m in range(bagsNumber): ####DECLARANDO MOCHILA DE "m" dimensões
        b = Knapsack(m)
        b.capacity = bagsCapacities[m]
        bags_List.append(b)
    """b1 = Knapsack(0,12210)
    b2 = Knapsack(1,12)
    bags_List.append(b1)
    bags_List.append(b2)"""
    # print(bag.capacity)
    house = House([], [], bags_List[0].capacity)
    masksize = 2 ###NAO MUDAR POR ENQUANTO (LINHA 93 PLAYER)
    mask = house.createFirstMask(masksize)
    #print("Mask:", mask)
    players_list = []

    for _ in range(25):  # DECLARANDO JOGADORES
        p = Player()
        p.createKnowledge(len(items_List))
        p.createRatings(mask)
        players_list.append(p)
    times = []
    _profits = []
    rounds = int(sys.argv[2]) #int(sys.argv[2])  ###NUMERO DE RODADAS
    z = 0
    tbest = 0
    bestProfit = 0 ###ATUAL LUCRO DA MELHOR SOLUÇÃO CONHECIDA
    bestWeight = [0]*bagsNumber ###ATUAL PESO DA MELHOR SOLUÇÃO CONHECIDA
    """for _ in range(bagsNumber):
        bestWeight.append(0)"""
    index = 0
    for p in house.best_so_far:  ##ATRIBUINDO VALOR A "bestWeight" E "bestProfit"
        if p == 1:
                            #weightSum += items_List[index].weight
            bestWeight = list(
                map(add, bestWeight, items_List[index].weight))
        index += 1
    bestProfit = house.bestProfit
    ########################## PRIMEIRA FASE #####################################
    for i in range(rounds):  # rounds' number
        """if i>8000:#bestWeight[0] > 5000 or bestWeight[1] > 5000 or bestWeight[2] > 5000 or bestWeight[3] > 5000 or bestWeight[4] > 5000:
            print("flaaaag")"""
        #print("Round number :", i)
        #print("Best solution so far:", house.best_so_far)
        #print("Profit :", house.profit(house.best_so_far))
        """if i > rounds/2 and _profits[-10]/_profits[-1] > 0.95:

            z = 1
            break"""
        dictbet = {}  ##DICIONARIO COM APOSTAS CONHECIDAS
        player_bets = [] ##APOSTAS DOS JOGADORES NESSA RODADA
        cacife_list = [] ##LISTA DE CACIFES DOS JOGADORES
        k = 1
        if i == 0:  ##PRIMEIRA RODADA
            house.createHouseProbs(players_list)
            for player in players_list:
                player.createRatings(mask)
                playerBet = player.bet(
                    house.best_so_far, house, bags_List, dictbet, bestWeight, bestProfit) ##APOSTA
                #bestWeight = playerBet[4]
                #bestProfit = playerBet[3]
                for bet in playerBet[-1]: ##ADICIONA APOSTAS DESCONHECIDAS AO DICIONARIO
                    if str(bet[2]) not in dictbet:
                        dictbet[bet[2]] = bet
                player_bets.append(playerBet)
                cacife_list.append(player.cacife)
                k += 1
            house.getFirstStats(players_list) ##PEGA INFORMACOES DOS PLAYERS
            #print("teste ", house.playerStats)

        else: ##DEMAIS RODADAS
            mask = house.createFirstMask(masksize)
            house.createHouseProbs(players_list)
            #print("Mask:", mask)
            for player in players_list:
                player.createRatings(mask)
                playerBet = player.bet(
                    house.best_so_far, house, bags_List, dictbet, bestWeight, bestProfit)
                
                for bet in playerBet[-1]:
                    if str(bet[2]) not in dictbet:
                        dictbet[bet[2]] = bet
                # print("player bet ", k, playerBet) #next iterations
                player_bets.append(playerBet)
                cacife_list.append(player.cacife)
                k += 1
        #print("player bets:", player_bets)
        house.settleBets(players_list, player_bets, items_List) ##RESOLVE AS APOSTAS
        for item in player_bets: ##SELECIONA NOVOS "bestWeight" E "bestProfit"
            if item[3] > bestProfit:
                bestProfit = item[3]
                bestWeight = item[4]
        _profits.append(bestProfit)
        times.append(time.time()-start)
        if i > 2 and _profits[-1] > _profits[-2]:
            tbest = times[-1]
        """print("Rounds' best:", house.best_so_far,
              house.profit(house.best_so_far))"""
        #print("Cacifes: ", cacife_list)

    ################################### SEGUNDA FASE #######################################
    end = time.time()
    #resultados_1fase_logger.info("Run %i: \t\tPeso Final = %s\tProfit: %f\tTempo: %fs\tOtimo: %f\nSolucao: %s\n" %(run+1, str(bestWeight), bestProfit, end-start, optimal, str(house.best_so_far)))
    #progresso_1fase_logger.info("Run %i: \nRodadas: %s\nTempos: %s\n" %(run+1, str(_profits), str(times)))
    phase1best = house.best_so_far
    resultados1_1fase.append(float(bestProfit))
    resultados2_1fase.append(float(tbest))
    totaltimes_1fase.append(float(end-start))
    resultados1_2fase = [0]
    #phase1bestWeight = bestWeight[:]
    #phase1bestProfit = float(bestProfit)
    t1 = times[-1]
    stats = []
    for item in house.playerStats:
        for p in item:
            stats.append(p)
    stats = sorted(stats, key=lambda i: i[1], reverse=True)
    for _ in range(10000):  # rounds segunda fase
        for i in range(2):  # 10 melhores jogadores
            candidate = [0]*len(house.best_so_far)
            n = len(house.best_so_far)-1
            for item in stats[i][0]:
                if item > random.random():
                    weightSum = []
                    for _ in range(bagsNumber):
                        weightSum.append(0)
                    index = 0
                    for p in candidate:
                        if p == 1:
                            #weightSum += items_List[index].weight
                            weightSum = list(
                                map(add, weightSum, items_List[index].weight))
                        index += 1
                    for i in range(len(weightSum)):
                        if weightSum[i] > bags_List[i].capacity:
                            break
                        elif weightSum[i] < bags_List[i].capacity and (i+1) == len(weightSum):
                            candidate[n] = 1
                n -= 1
            probe = House.profit(house, candidate)
            if probe > resultados1_2fase[-1]:
                resultados1_2fase.append(probe)
            if probe > House.profit(house, house.best_so_far):
                house.best_so_far = candidate
                bestWeight = weightSum[:] ###ATENCAO AQUI
                bestProfit = float(probe)
        _profits.append(house.profit(house.best_so_far))
        times.append(time.time()-start)
        if _profits[-1] > _profits[-2]:
            tbest = times[-1]
    t2 = times[-1]
    #house.best_so_far = phase1best
    _profits2 = [house.profit(phase1best)]
    times2 = [time.time()+t1-t2-start]
    #####################################################################
    """for i in range(rounds*2):  # rounds' number
        if time.time()-start-t2+t1 > t2:
            break
        #print("Round number :", i)
        #print("Best solution so far:", house.best_so_far)
        #print("Profit :", house.profit(house.best_so_far))
        _profits2.append(house.profit(house.best_so_far))
        times2.append(time.time()-start-t2+t1)
        player_bets = []
        cacife_list = []
        dictbet = {}
        k = 1
        if i == 0:
            house.createHouseProbs(players_list)
            for player in players_list:
                player.createRatings(mask)
                playerBet = player.bet(house.best_so_far, house, bags_List,dictbet)
                for bet in playerBet[-1]:
                    if str(bet[2]) not in dictbet:
                        dictbet[bet[2]] = bet
                # print("player bet ", k, playerBet) #1st iteration
                player_bets.append(playerBet)
                cacife_list.append(player.cacife)
                k += 1
            house.getFirstStats(players_list)
            #print("teste ", house.playerStats)

        else:
            mask = house.createFirstMask(masksize)
            house.createHouseProbs(players_list)
            #print("Mask:", mask)
            for player in players_list:
                player.createRatings(mask)
                playerBet = player.bet(house.best_so_far, house, bags_List,dictbet)
                for bet in playerBet[-1]:
                    if str(bet[2]) not in dictbet:
                        dictbet[bet[2]] = bet
                # print("player bet ", k, playerBet) #next iterations
                player_bets.append(playerBet)
                cacife_list.append(player.cacife)
                k += 1
        #print("player bets:", player_bets)
        house.settleBets(players_list, player_bets, items_List)
        #print("Rounds' best:", house.best_so_far, house.profit(house.best_so_far))
        #print("Cacifes: ", cacife_list)"""

    # cortei
    #print("Best solution:", house.best_so_far, house.profit(house.best_so_far))
    # for item in bags_List:
    # print(item.capacity)

    #print(_profits)
    """
    print(times)
    print(_profits2)
    print(times2)"""
    #print("optimal: ", optimal)
    """candidateBet = house.best_so_far
    weightSum = []
    for _ in range(bagsNumber):
        weightSum.append(0)
    index = 0
    for item in candidateBet:
        if item == 1:
            #weightSum += items_List[index].weight
            weightSum = list(map(add, weightSum, items_List[index].weight))
        index += 1
    #print("ws: ", weightSum)"""
    #print("omg",bestWeight, _profits)
    end = time.time()
    #print(t2)
    resultados1.append(float(bestProfit))
    resultados2.append(float(tbest))
    totaltimes.append(float(end-start))
    """plt.plot(range(0,int(sys.argv[2])), _profits, color='green', label='Somente 1ª fase')
    #plt.axvline(x=t1, color='r', linestyle='--', label='Final da 1ª fase')
    plt.axhline(y=optimal, color='brown', label='optimal')
    plt.xlabel('Rodadas', fontsize=12)
    plt.ylabel('Lucro', fontsize=12)
    plt.legend()
    plt.title(datafile)
    plt.savefig(str(datafile)+'_'+'run'+str(run)+'.png')
    plt.cla()
    plt.clf()"""
    output_andre_logger.info("%d\t%d\t%d\t%d\t%f" %(_profits[-1], resultados1_1fase[-1], resultados1_2fase[-1], resultados1_2fase[-1], time.time()-start))
    #progresso_logger.info("Run %i: \nRodadas: %s\nTempos: %s\n" %(run+1, str(_profits), str(times)))
    #resultados_logger.info("Run %i: \t\tPeso Final = %s\tProfit: %f\tTempo: %fs\tOtimo: %f\nSolucao: %s\n" %(run+1, str(bestWeight), bestProfit, end-start, optimal, str(house.best_so_far)))
    
#print("resultados",resultados1)
#print(resultados2)

#resultados_logger.info("\n\nProfit: %f\tMAX: %f\tMIN: %f\tOTIMO: %f\t%%MEDIA: %f\t%%MELHOR: %f\t TEMPO MELHOR: %fs\t TEMPO TOTAL: %fs\t\t%d/%d/%d\t%d:%d:%d\n\n\n\n" % (mean(resultados1), max(resultados1), min(resultados1),optimal, (optimal-mean(resultados1))/optimal, (optimal-max(resultados1))/optimal, mean(resultados2), mean(totaltimes), now.day, now.month, now.year, now.hour, now.minute, now.second))
#resultados_1fase_logger.info("\n\nProfit: %f\tMAX: %f\tMIN: %f\tOTIMO: %f\t%%MEDIA: %f\t%%MELHOR: %f\t TEMPO MELHOR: %fs\t TEMPO TOTAL: %fs\t\t%d/%d/%d\t%d:%d:%d\n\n\n\n" % (mean(resultados1_1fase), max(resultados1_1fase), min(resultados1_1fase),optimal, (optimal-mean(resultados1_1fase))/optimal, (optimal-max(resultados1_1fase))/optimal, mean(resultados2_1fase), mean(totaltimes_1fase), now.day, now.month, now.year, now.hour, now.minute, now.second))

print("Terminou problema ", datafile)
print("tempo total:", end-start)
#print(house.best_so_far,house.bestProfit)
#print(_profits,bestProfit,bestWeight)
"""if z == 1:
    print("terminou primeira fase antecipadamente")
print("tempo pra melhor: ", tbest)"""
"""plt.plot(times, _profits, color='blue', label='1ª e 2ª fases')
plt.plot(times2, _profits2, color='green',
         linestyle='--', label='Somente 1ª fase')
plt.axvline(x=t1, color='r', linestyle='--', label='Final da 1ª fase')
plt.axhline(y=optimal, color='brown', label='optimal')
plt.xlabel('t (s)', fontsize=12)
plt.ylabel('Lucro', fontsize=12)
plt.legend()
plt.title(datafile)
plt.show()"""



#print(resultados1)

""" 
print("ratings:")
for p in players_list:
    print(p.ratings) 
"""

# house.createHouseProbs(players_list)

""" 
p1 = Player()
p1.createKnowledge(len(items_List))
p1.createRatings(mask)
players_list.append(p1)

house.createHouseProbs(players_list) 
"""

"""for p in players_list:
    # print("RATING:", p.ratings)
    print(p.bet(house.best_so_far, house, bag))
    # p.bet(house.best_so_far,house)"""
