class Timer():

    def __init__(self) -> None:
        pass
    
    def __iter__(self):
        self.hour = 0
        self.day = 1
        self.month = 1
        self.m_day_counter = 1
        self.months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return self

    def __next__(self):
        if self.day <= 365:
            _dt = (self.hour, self.day, self.month)
            if self.hour >= 24:
                self.hour = 0
                self.day += 1
                self.m_day_counter += 1
                if self.m_day_counter > self.months_days[self.month - 1]:
                    self.m_day_counter = 1
                    self.month += 1
            else:
                self.hour += 1
        else:
            raise StopIteration