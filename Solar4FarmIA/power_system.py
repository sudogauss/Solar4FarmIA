from const import *
from typing import Tuple


class PowerSystem():

    def __init__(self, 
                 solar_area: float,
                 solar_efficiency: float,
                 production_country: str,
                 max_power: int,
                 material: str) -> None:
        
        self.__solar_area = solar_area
        self.__solar_efficiency = solar_efficiency
        self.__production_country = production_country
        self.__max_power = max_power
        self.__material = material

        self.__max_battery_capacity = CAPACITY_COEFFICIENT * (self.max_power / OPERATION_VOLTAGE)
        self.__main_battery_capacity = self.__max_battery_capacity
        self.__backup_battery_capacity = self.__max_battery_capacity
        self.__on_main_battery = True

        self.__total_battery_energy = 0

        self.__low_threshold = DISCHARGE_THRESHOLD * self.__max_battery_capacity
        self.__high_threshold = CHARGE_THRESHOLD * self.__max_battery_capacity

        assert self.__high_threshold > ACTIVE_CURRENT

    def get_carbon_footprint(self) -> float:

        solar_panel_footprint = (self.__max_power 
                * (PRODUCTION_COUNTRY_TO_FOOTPRINT[self.__production_country] 
                    + PRODUCTION_MATERIAL_TO_FOOTPRINT[self.__material]) / 2) \
                + (PRODUCTION_COUNTRY_DISTANCE[self.__production_country] * KM_TO_CARBON_FOOTPRINT)
        
        battery_footprint = self.__total_battery_energy * ENERGY_TO_FOOTPRINT

        return solar_panel_footprint + battery_footprint

    def __simulate_power_system(self, load_current: float, solar_current: float) -> Tuple[bool, bool]:

        if self.__on_main_battery:
            if self.__main_battery_capacity >= load_current and self.__main_battery_capacity >= self.__low_threshold:
                self.__main_battery_capacity -= load_current
                self.__total_battery_energy += load_current
                if solar_current >= (self.__max_battery_capacity / 2):
                    self.__backup_battery_capacity += (self.__max_battery_capacity / 2)
                    self.__backup_battery_capacity = min(self.__backup_battery_capacity, self.__max_battery_capacity)
                return (True, False)
            else:
                self.__on_main_battery = False
                return (False, True)                     
        else:
            if self.__backup_battery_capacity >= load_current:
                self.__backup_battery_capacity -= load_current
                self.__total_battery_energy += load_current
                if solar_current >= (self.__max_battery_capacity / 2):
                    self.__main_battery_capacity += (self.__max_battery_capacity / 2)
                    self.__main_battery_capacity = min(self.__main_battery_capacity, self.__max_battery_capacity)
                return (True, False)
            else:
                if self.__main_battery_capacity >= self.__high_threshold:
                    self.__on_main_battery = True
                    return (False, True)
                else:
                    return (False, False)



    def next_step(self, load_current: float, solar_state: Tuple[float, float]) -> bool:

        _solar_current = (solar_state[1] * self.__solar_area) * self.__solar_efficiency / OPERATION_VOLTAGE

        _satisfy, _switch = self.__simulate_power_system(load_current, _solar_current)
        
        if _switch:
            _satisfy, _switch = self.__simulate_power_system(load_current, _solar_current)

        assert _switch == False

        return _satisfy


        
                            
            
