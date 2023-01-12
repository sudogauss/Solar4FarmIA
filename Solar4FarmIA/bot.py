import numpy as np
from const import ACTIVE_CURRENT, PASSIVE_CURRENT, \
            BOT_ACTIVITY_BEGINNING, BOT_ACTIVITY_FINISHING
import sys


class Bot():

    def __init__(self, 
                 initial_probability: float, 
                 dp_winter: float, 
                 dp_spring: float, 
                 dp_summer: float,
                 dp_fall: float) -> None:
        """
        Allows to initialize activation probabilty and probabilities
        discrete steps for each season 

        Args:
            initial_probability (float): probability after activity
            dp_winter (float): winter's probabilty discrete step
            dp_spring (float): spring's probabilty discrete step
            dp_summer (float): summer's probabilty discrete step
            dp_fall (float): fall's probabilty discrete step
        """
        
        assert(0.0 <= initial_probability <= 1.0)

        self.initial_probability = initial_probability
        self.probability = initial_probability

        self.dpw = dp_winter
        self.dpsp = dp_spring
        self.dps = dp_summer
        self.dpf = dp_fall

    def next_step(self, hour: int, month: int) -> float:
        _p = self.probability
        _x = np.uniform(0.0, 1.0)
        _is_active = (0.0 <= _x <= _p)

        if _is_active:
            self.probability = self.initial_probability
            return ACTIVE_CURRENT
        else:
            if BOT_ACTIVITY_BEGINNING <= hour <= BOT_ACTIVITY_FINISHING:
                if month == 12 or 1 <= month <= 2:
                    self.probability += self.dpw
                elif 3 <= month <= 5:
                    self.probability += self.dpsp
                elif 6 <= month <= 8:
                    self.probability += self.dps
                elif 9 <= month <= 11:
                    self.probability += self.dpf
                else:
                    print("Error in bot simulation: month number {month} does not exist")
                    sys.exit(1)
                
                if self.probability > 1.0:
                    self.probability = 1.0
            
            elif 0 <= hour <= BOT_ACTIVITY_BEGINNING or BOT_ACTIVITY_FINISHING <= hour < 24:
                pass
            else:
                print("Error in bot simulation: hour {month} does not exist")
                sys.exit(1)
            
            return PASSIVE_CURRENT
