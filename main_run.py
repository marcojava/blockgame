#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 20:04:51 2022

@author: marcoj
"""


from class_agent import agent
from numpy import *
from numpy.core.numeric import zeros

import game_functions
import random
from random import *


def define_int_J(x,N):
    
    neigh_list = []
    
    n_side = int(sqrt(N))
    
    n_1 = x + 1
    
    if ((n_1 - N)%n_side) == 0:
        
        n_1 -= n_side
    
    n_2 = x + n_side
    
    if n_2 > N-1:
        
        n_2 -= N
    
    n_3 = x - 1
    
    if (x%n_side) == 0:
        
        n_3 += n_side
    
    
    n_4 = x - n_side
    
    if n_4 < 0:
        
        n_4 += N
    

    neigh_list.append(n_3)
    neigh_list.append(n_1)
    neigh_list.append(n_2)
    neigh_list.append(n_4)
        
    
    return neigh_list


def generate_lattice_list(N,miner_p):
    
    nr_miners = int(N*miner_p)
    
    miner_indices = sample(range(0, N), nr_miners)
    
    #print(miner_indices)
    
    agent_list = []


    x = 0

    strategy = 1

    while x < N:


        int_J = 0

        neighs = define_int_J(x,N)  

        agent_list.append(agent(x,strategy,neighs))

        if x in miner_indices:
            strategy=-1
        else:
            strategy = 1
    
        x+=1
    
    
    return agent_list


###
###Game Parameters
    
nr_agent = 400 #Number of agents
beta = 0.5#Noise
miner_p = 0.5#Probability of miners at t=0
electric_cost = 100#cost of electricity
brc = 50#conversion parameter
reward = 130#miners' reward



######
####Simulation steps
MC_steps = 100*nr_agent#nr of time steps for a single simulation run
nr_attempts = 1#nr of simulations
##############
#############

test_mc = 0


while test_mc < nr_attempts:
    
    
    agent_list = []
    miners_payoff = []
    users_payoff = []
    agent_list = generate_lattice_list(nr_agent,miner_p)

    strategy_list = []

    miners_over_time = []

    for x in agent_list:
        
        strategy_list.append(x.strategy)


    nr_step = 0

    number_miners = 0.0
    number_miners = strategy_list.count(-1)
    

    miners_over_time.append(number_miners/nr_agent)
    
    
    while nr_step < MC_steps:
        
        count_payoff_miner = 0.0
        count_payoff_user = 0.0

        next_strategies = []    

        for y in agent_list:
        
            next_strategies.append(game_functions.update_strategy(y,strategy_list,agent_list,beta,brc,reward,electric_cost))
            
            if y.strategy==-1:
                
                
                count_payoff_miner += y.payoff
            else:
                count_payoff_user += y.payoff
                
        if number_miners>0:    
            count_payoff_miner/= number_miners
        count_payoff_user/= (nr_agent-number_miners)
        miners_payoff.append(count_payoff_miner)
        users_payoff.append(count_payoff_user)
        ww=0
        for w in agent_list:
            w.SetStrategy(next_strategies[ww])
            
            
            
            ww+=1
    
        number_miners = next_strategies.count(-1)
    
        next_strategies = copy(strategy_list)
        miners_over_time.append(number_miners/nr_agent)
    
        nr_step+=1
    
    
    
    ###The density of miners saved in external text file. File_name depends of local machine
    file_name = 'sim/m_density.txt'

    with open(file_name, 'w') as f:
        for item in miners_over_time:
            f.write("%s\n" % item)
    
    
    
   
    test_mc+=1
