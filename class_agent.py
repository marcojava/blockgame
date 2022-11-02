class agent:
    
    def __init__(self, name,strategy,neigh_list):
    
        self.name = name
        self.strategy = strategy#1 users, -1 miners 
        
        
        self.neigh_list = neigh_list
        self.payoff = 0.0
        
        
    
    def SetStrategy(self,new_strategy):
    
        self.strategy = new_strategy
    
    def SetPayoff(self,new_payoff):
        
        self.payoff = new_payoff
    
    def ResetPayoff(self):
        
        self.payoff = 0
    
    