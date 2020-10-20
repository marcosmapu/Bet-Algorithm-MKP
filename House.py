from Knapsack import firstGreedyChoice
import random
import Item
from Player import Player

class House:
    def __init__(self, players_list: list, nPicks: list, firstCapacity: float, mask = [], trSize = 1, playerStats = [], bestProfit = 0):
        self.players_list = players_list
        self.nPicks = nPicks
        self.mask = mask
        self.trSize = trSize
        self.bestProfit = bestProfit
        self.bankCacife = float("inf")
        self.houseProbs = []
        self.firstCapacity = firstCapacity
        self.best_so_far = firstGreedyChoice(self.firstCapacity)[2]
        self.playerStats = playerStats

    def createFirstMask(self, size=3):
        if len(self.best_so_far) <= 0:
            best_so_far = firstGreedyChoice(self.firstCapacity)[2]
            maskLimit = len(best_so_far)
            self.best_so_far = best_so_far
        else:
            maskLimit = len(self.best_so_far)

        #print("USED:", self.best_so_far, "To make the mask")
        mask = random.sample(range(maskLimit), size)
        self.mask = mask
        return self.mask


    def createHouseProbs(self, players_list = []):
        sums = []
        for m in range(2**len(self.mask)):            
            total = 0
            for p in players_list:
                total += p.ratings[m]
            sums.append(total)        
        # print("\nSUMS:",sums)
        # len(players_list)*(2**len(self.mask))
        # HouseProbs = list(map(lambda x: (1/x), sums))
        houseProbs = list(map(lambda x: (x/len(players_list)), sums))
        # print("\nBANKQUOT:",houseProbs)
        self.houseProbs = houseProbs
        return self.houseProbs


    def best(self):
        pass
    
    def profit(self, solution: list):
        solProfit = 0
        index = 0
        for item in solution:
            if item == 1:
                solProfit += Item.items_List[index].profit
            index += 1
        return solProfit
    
    def getFirstStats(self, players_list: list):
        for player in players_list:
            self.playerStats.append([[player.knowledge,0,0]]) #create list with player's initial stats

    def settleBets(self, players_list: list, player_bets: list, items_List: list):
        i = 0
        winners = []
        #each bet is one of the indiviual player bets
        
        for item in player_bets:  
            if item[3] > self.bestProfit:
                self.best_so_far = item[0]
                self.bestProfit = item[3]
                winners = []
                winners.append(i) #add new winner
            elif item[3] > self.bestProfit and winners != []:
                winners.append(i) #add winners tied with former winners
            self.playerStats[i][-1][1] += 1 #number of survived rounds for each player
            i += 1
        for player in winners:
            #print("winners", winners)
            players_list[player].cacife += player_bets[player][1]*(1+self.houseProbs[player_bets[player][2]]) #pay winners accordingly to house odds
            self.playerStats[player][-1][2] += 1 #number of won rounds fo each player
        i = 0
        for player in players_list:
            if player.cacife == 0: #checking if necessary to reset players
                Player.reset(player)
                Player.createKnowledge(player, len(items_List))
                Player.createRatings(player, self.mask)
                self.playerStats[i].append([player.knowledge,0,0])
            i += 1
                
                