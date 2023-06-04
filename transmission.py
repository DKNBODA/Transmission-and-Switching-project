import math
import numpy as np
from math import factorial

N = [3,4,7,9,12,13]
n60 = [2,1,1,1,1,1]
n120 = [3,2,2,2,2,2]
n180 = [4,3,3,3,3,3]

def erlang(A, m):
    L = (A ** m) / factorial(m)
    sum_ = 0
    for n in range(m + 1): sum_ += (A ** n) / factorial(n)
    block=(L / sum_)
    return block 
    
    
def getacell(block_prob, trunks):
    left = 0
    right = 1000

    # Perform binary search to find the minimum offered load with the desired blocking probability
    while True:
        mid = (left + right) / 2
        b = erlang(mid, trunks)
        if abs(b - block_prob) < 0.0001:
            return mid
        elif b > block_prob:
            right = mid
        else:
            left = mid


def calculatecells(blockingprobability,totalnoofslots,slotsperuser,numberofchannelspercluster,citysize, noofsubscribers, avgcallperuser, avgcallduration, interferenceRatio):
    
    
        
    
    auser=(avgcallperuser/(24*60))*avgcallduration
    
    minimumreusefactor=(interferenceRatio*6)/3
    
    CI=minimumreusefactor/6
    
    trunks=math.floor((numberofchannelspercluster/minimumreusefactor)*(totalnoofslots/slotsperuser))
   
    acell=getacell(blockingprobability,trunks)
    
    noofsubscriberspercell=math.floor(acell/auser)
    
    totalcellsincity=math.ceil(noofsubscribers/noofsubscriberspercell)
    
    print("total number of cells without sectoring",totalcellsincity)
   
    
    bestN=[]
    bestn=[]
    
    i = 0
    while i<len(N):
        v = N[i] / n120[i]
        if v > CI:
            bestN.append(N[i])
            bestn.append(n120[i])
            break
        else:
            i += 1
    i = 0
    while i<len(N):
        v = N[i] / n60[i]
        if v > CI:
            bestN.append(N[i])
            bestn.append(n60[i])
            break
        else:
            i += 1
    i = 0
    while i<len(N):
        v = N[i] / n180[i]
        if v > CI:
            bestN.append(N[i])
            bestn.append(n180[i])
            break
        else:
            i += 1  
    
    trunks120=math.floor(((numberofchannelspercluster/bestN[0])*(totalnoofslots/slotsperuser))/3)
    trunks60 =math.floor(((numberofchannelspercluster/bestN[1])*(totalnoofslots/slotsperuser))/6)
    trunks180=math.floor(((numberofchannelspercluster/bestN[2])*(totalnoofslots/slotsperuser))/2) 
    
    
   
    
   
    acell120=getacell(blockingprobability,trunks120)
    noofsubscriberspercell120=math.floor(acell120*3/auser)
      
   
    acell60=getacell(blockingprobability,trunks60)
    noofsubscriberspercell60=math.floor(acell60*6/auser)
       
  
    acell180=getacell(blockingprobability,trunks180)
    noofsubscriberspercell180=math.floor(acell180*2/auser)
    
    if noofsubscriberspercell120>noofsubscriberspercell60 and noofsubscriberspercell120>noofsubscriberspercell180:
        print("best sectoring is 120")
        totalcellsincity=math.ceil(noofsubscribers/noofsubscriberspercell120)
    elif  noofsubscriberspercell60>noofsubscriberspercell120 and noofsubscriberspercell60>noofsubscriberspercell180: 
        totalcellsincity=math.ceil(noofsubscribers/noofsubscriberspercell60)
        print("best sectoring is 60")
    else:
        totalcellsincity=math.ceil(noofsubscribers/noofsubscriberspercell180)
        print("best sectoring is 180")
    
        
        
       
            
    return totalcellsincity

blockingprobability=0.001
totalnoofslots=8
slotsperuser=2
numberofchannelspercluster = 125
citysize = 450  # in Km2
noofsubscribers=1000000#number of subscribers per city
avgcallperuser = 10 #calls per day
avgcallduration = 1  # in minutes
interferenceRatio = 6.25


cells = calculatecells(blockingprobability,totalnoofslots,slotsperuser,numberofchannelspercluster,citysize, noofsubscribers, avgcallperuser, avgcallduration, interferenceRatio)

print("number of total cells after sectoring",cells)
    
    
    
    
    
    
    
    