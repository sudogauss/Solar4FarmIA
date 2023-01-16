from Solar4FarmIA.const import MONTHS_DAYS
from typing import Tuple


class Timer():
    """
        Timer iterator class which allows to count hour by hour
        during the year keeping track of hours, days and months.

        Attributes:
            hour (int): current hour
            day (int): current day
            month (int): current month
            m_day_counter (int): day counter in current month
            months_days List[int]: day's number for each month
    """

    def __init__(self) -> None:
        pass
    
    def __iter__(self):
        """
        Initializes iterator

        Returns:
            Timer: timer iterator
        """
        self.hour = 0
        self.day = 1
        self.month = 1
        self.m_day_counter = 1
        return self

    def __next__(self) -> Tuple[int, int, int]:
        """
        Allows to iterate through the year keeping track
        of day and month

        Raises:
            StopIteration: stops the iteration
        """
        if self.day <= 365:
            _dt = (self.hour, self.day, self.month)
            if self.hour >= 23:
                self.hour = 0
                self.day += 1
                self.m_day_counter += 1
                if self.m_day_counter > MONTHS_DAYS[self.month - 1]:
                    self.m_day_counter = 1
                    self.month += 1
            else:
                self.hour += 1
            return _dt
        else:
            raise StopIteration