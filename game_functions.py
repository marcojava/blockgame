from class_agent import agent
from numpy import *
import math
import random as rand
from random import uniform, random, choices, sample, randrange



def update_strategy_list(agent_list):
    
    s_list = []
    
    
    for k in agent_list:
        
        s_list.append(k.strategy)
    
    
    return s_list
    
    

def compute_payoff(x,strategy_list,population,brc_v,rwd,e_cost):
    
    group = 4
    
    N = len(population)
    
    
    agent_neighs = x.neigh_list
    
    
    
    count_local_users = 0.0
    
    for y in agent_neighs:
        
        if population[y].strategy == 1:
            
            count_local_users+=1
    
    payoff = 0.0
    opposite_payoff = 0.0
    
    miner_density = 0.0
    
    strategy_list = []
    for xx in population:
        
        strategy_list.append(xx.strategy)
        
    nr_users = strategy_list.count(1)
    
    nr_miners = N - nr_users
    user_density = nr_users / N
    
    miner_density = 1.0 - user_density
    
    
    if nr_miners >0:
        reward = rwd/nr_miners
    else:
        reward = 0
    
    
    brc = brc_v
    
    benefit_cost_ratio = brc
    
    electric_cost = e_cost / brc
    
    user_tax = 0.1
    
    if x.strategy == 1:
        if miner_density == 0.0:
            payoff = 0.0 
            opposite_payoff = 0.0
            
        elif miner_density > 0:
            
           
            
            payoff  = (1.0/miner_density)*((float(count_local_users)+1)*user_tax/5) - user_tax
            
            if count_local_users == 0:
                payoff = 0
            
            var_group= 0
            side_payoff = 0.0
            while var_group < group:
                
                central_neigh_index = agent_neighs[var_group]
                central_neigh = population[central_neigh_index]
                
                neighs_of_neigh = central_neigh.neigh_list
                
                neigh_count_local_users = 0
                for yy in neighs_of_neigh:
        
                    if population[yy].strategy == 1:
            
                        neigh_count_local_users+=1
                
                side_payoff = side_payoff + (1.0/miner_density)*((float(neigh_count_local_users)*user_tax+1)/5) - user_tax
                
                if neigh_count_local_users == 0:
                    side_payoff = 0
                
                var_group+=1
            
            payoff+= side_payoff
            
            opposite_payoff = reward - electric_cost
            
            
    
    elif x.strategy == -1:
        
        if user_density == 0.0:
            payoff = 0.0 
            opposite_payoff = 0.0
        else:
            payoff = reward - electric_cost
        
        
            opposite_payoff = (1.0/miner_density)*(float(count_local_users)*user_tax/5) - user_tax
            
            if count_local_users == 0:
                opposite_payoff = 0
            
            
            
            var_group= 0
            side_payoff = 0.0
            while var_group < group:
                
                central_neigh_index = agent_neighs[var_group]
                central_neigh = population[central_neigh_index]
                
                neighs_of_neigh = central_neigh.neigh_list
                
            
                neigh_count_local_users = 0
                for yy in neighs_of_neigh:
        
                    if population[yy].strategy == 1:
            
                        neigh_count_local_users+=1
                
                side_payoff = side_payoff + (1.0/miner_density)*((float(neigh_count_local_users)*user_tax)/5) - user_tax
                
                if neigh_count_local_users == 0:
                    side_payoff = 0
                
                var_group+=1
            
            opposite_payoff+= side_payoff
        
  
    
    return payoff,opposite_payoff



def update_strategy(x,strategy_list,population,beta,brc,rew,electric_cost):
    
    previous_payoff = x.payoff
    current_strategy = x.strategy
    
   
    
    new_payoff,opposite_payoff = compute_payoff(x, strategy_list, population,brc,rew,electric_cost)
    
    
    
    diff_payoff = opposite_payoff-new_payoff
    
    
    update_prob = (1 + exp(-beta*diff_payoff))**(-1)
    
    
    stay_prob = 1.0 - update_prob
    
    
    
    next_strategy_prob=choices([0,1], [update_prob,stay_prob])
    
    
    
    
    new_strategy = current_strategy 
    if next_strategy_prob[0] == 0:
        new_strategy = current_strategy*(-1)
    
    
    x.SetPayoff(new_payoff)
    return new_strategy
