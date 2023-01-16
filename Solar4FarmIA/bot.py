import numpy as np
from Solar4FarmIA.const import ACTIVE_CURRENT, PASSIVE_CURRENT, \
            BOT_ACTIVITY_BEGINNING, BOT_ACTIVITY_FINISHING
import sys


class Bot():
    """
    This class allows to simulate FarmBot activity. It has 2 modes of functionning:
    active and passive. The power consumption is bigger for active mode (see pdf in docs folder
    in this repository). Depending on season(month) and solar activity 
    (dusk and dull, hour of the day) bot's activation probabilty increases.

    Attributes:
            probability (float): current activation probability
            initial_probability (float): probability after activity
            dp_winter (float): winter's probabilty discrete step
            dp_spring (float): spring's probabilty discrete step
            dp_summer (float): summer's probabilty discrete step
            dp_fall (float): fall's probabilty discrete step
    """

    def __init__(self, 
                 initial_probability: float, 
                 dp_winter: float, 
                 dp_spring: float, 
                 dp_summer: float,
                 dp_fall: float) -> None:
        """
        Allows to initialize activation probabilty and probabilities
        discrete steps for each season. Keep initial probabilty in the 
        interval [0.001, 0.01] and discrete steps in the interval [0.01, 0.05]

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
        """
        This function allows to simulate the behaviour of FarmBot for
        each hour and month. It progressively increases the probability
        of activation and resets the probability after its activation.

        Args:
            hour (int): hour of the day
            month (int): month of the year

        Returns:
            float: Electrical current used by bot (passive or active current)
        """
        _p = self.probability
        _x = np.uniform(0.0, 1.0)
        _is_active = (0.0 <= _x <= _p) # probabilistic activation

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
                print("Error in bot simulation: hour {hour} does not exist")
                sys.exit(1)
            
            return PASSIVE_CURRENT
