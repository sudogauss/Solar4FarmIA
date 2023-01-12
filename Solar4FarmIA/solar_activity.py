import pandas as pd
from typing import Tuple
import numpy as np

from const import TEMPERATURE_STATE_NUMBER, IRRADIANCE_STATE_NUMBER



class SolarActivity():
    """
    This class allows to simulate solar activaty for each season of the year
    with Markov chains. We use real world data for Paris (but you can choose any region
    using fetch script in data folder). We keep track of solar temperature and irradiance
    which we refer as current_state. Data used is provided by NSRDB. The code is based on 
    NSRDB's csv structure. Choose Temerature, DNI and DHI on download. Temperature can be used
    for more precise battery or solar panel behaviour simulation, but it is not currently used.

    Attributes:
        __current_state (Tuple[float, float]): current state (temperature, irradiance)
        __summer_transition_matrix (np.matrix): transition matrix for summer season
        __spring_transition_matrix (np.matrix): transition matrix for spring season
        __fall_transition_matrix (np.matrix): transition matrix for fall season
        __winter_transition_matrix (np.matrix): transition matrix for winter season
        Tmin (float): minimal temperature
        Tmax (float): maximal temperature
        Rmin (float): minimal irradiance
        Rmax (float): maximal irradiance
        dT (float): temperature discrete step
        dR (float): irradiance discrete step
    """
    def __init__(self, initial_state: Tuple[float, float], solar_dataset: str = "data/solar_data_2018.csv") -> None:
        """
        SolarActivity constructor allows to build transition matrcies for each season
        based on solar_dataset. Initilisez __curent_state to initial_state.

        Args:
            initial_state (Tuple[int, int]): Initial solar temperature and 
            solar_dataset (str): Solar dataset file. Defaults to solar_data_2018.csv
        """
        self.__current_state = initial_state
        solar_df = pd.read_csv(solar_dataset)
        months = np.array(list(map(lambda x: int(x), solar_df["Location ID"].to_list()[2:])))
        # day = np.array(list(map(lambda x: int(x), solar_df["City"].to_list()[2:]))) # uncomment to use days
        # hours = np.array(list(map(lambda x: int(x), solar_df["State"].to_list()[2:]))) # uncomment to use hours 
        temperatures = np.array(list(map(lambda x: float(x), solar_df["Longitude"].to_list()[2:])))
        irradiances = np.array(list(map(lambda x: float(x), solar_df["Latitude"].to_list()[2:])))

        self.Tmin, self.Tmax = temperatures.min(), temperatures.max()
        self.Rmin, self.Rmax = irradiances.min(), irradiances.max()

        self.dT = (self.Tmax - self.Tmin) / TEMPERATURE_STATE_NUMBER # discrete step of temperature
        self.dR = (self.Rmax - self.Rmin) / IRRADIANCE_STATE_NUMBER # discrete step of irradiance

        N = (TEMPERATURE_STATE_NUMBER * IRRADIANCE_STATE_NUMBER) # state number

        self.__summer_transition_matrix = np.ones((N, N))
        self.__spring_transition_matrix = np.ones((N, N))
        self.__fall_transition_matrix = np.ones((N, N))
        self.__winter_transition_matrix = np.ones((N, N))


        for i in range(len(temperatures) - 1):
            j = int((temperatures[i] - self.Tmin) / self.dT)
            k = int((irradiances[i] - self.Rmin) / self.dR)
            s = int((temperatures[i+1] - self.Tmin) / self.dT)
            t = int((irradiances[i+1] - self.Rmin) / self.dR)

            if j == TEMPERATURE_STATE_NUMBER: # decrement for maximal value as it exceeds the range
                j -= 1
            if k == IRRADIANCE_STATE_NUMBER:
                k -= 1
            if s == TEMPERATURE_STATE_NUMBER:
                s -= 1
            if t == IRRADIANCE_STATE_NUMBER:
                t -= 1

            month = months[i]

            _from_state = j*IRRADIANCE_STATE_NUMBER + k
            _to_state = s*IRRADIANCE_STATE_NUMBER + t

            if month == 12 or 1 <= month <= 2:
                self.__winter_transition_matrix[_from_state][_to_state] += 1
            elif 3 <= month <= 5:
                self.__spring_transition_matrix[_from_state][_to_state] += 1
            elif 6 <= month <= 8:
                self.__summer_transition_matrix[_from_state][_to_state] += 1
            elif 9 <= month <= 11:
                self.__fall_transition_matrix[_from_state][_to_state] += 1
            else:
                print("Error in transition matrix constrution: month number {month} does not exist")

        winter_cols_sums = self.__winter_transition_matrix.sum(axis=0)
        spring_cols_sums = self.__spring_transition_matrix.sum(axis=0)
        fall_cols_sums = self.__fall_transition_matrix.sum(axis=0)
        summer_cols_sums = self.__summer_transition_matrix.sum(axis=0)

        for i in range(N):
            for j in range(N):
                self.__winter_transition_matrix[i][j] /= winter_cols_sums[j]
                self.__spring_transition_matrix[i][j] /= spring_cols_sums[j]
                self.__fall_transition_matrix[i][j] /= fall_cols_sums[j]
                self.__summer_transition_matrix[i][j] /= summer_cols_sums[j]

    def next_step(self) -> Tuple[float, float]:
        """
        A function to be called to return current state and transit to the next state

        Returns:
            Tuple[float, float]: current state
        """
        _st = self.__curent_state 
        __next_state()
        return _st

    def __next_state(self, month: int) -> None:
        """
        Transits __current_state to a new state using the transition matrices 
        corresponding to the season.

        Args:
            month (int): a month of the year
        """
        j = int((self.current_state[0] - self.Tmin) / self.dT)
        k = int((self.current_state[1] - self.Rmin) / self.dR)

        if j == TEMPERATURE_STATE_NUMBER: # decrement for maximal value as it exceeds the range
            j -= 1
        if k == IRRADIANCE_STATE_NUMBER:
            k -= 1

        _st = j * IRRADIANCE_STATE_NUMBER + k
        h = np.random.uniform(0.0, 1.0)
        acc = 0.0
        _new_st = 0

        for l in range(N-1):
            _tmp_trans = 0.0
            if month == 12 or 1 <= month <= 2:
                _tmp_trans = self.__winter_transition_matrix[_st][l]
            elif 3 <= month <= 5:
                _tmp_trans = self.__spring_transition_matrix[_st][l]
            elif 6 <= month <= 8:
                _tmp_trans = self.__summer_transition_matrix[_st][l]
            elif 9 <= month <= 11:
                _tmp_trans = self.__fall_transition_matrix[_st][l]
            else:
                print("Error in transition matrix constrution: month number {month} does not exist")

            if acc <= h <= acc + _tmp_trans:
                _new_st = l
                break

            acc += _tmp_trans

        _j = int(_new_st / IRRADIANCE_STATE_NUMBER)
        _k = _new_st % IRRADIANCE_STATE_NUMBER

        self.current_state = (self.Tmin + _j * self.dT, self.Rmin + _k * self.dR) 
