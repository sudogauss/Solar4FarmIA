PASSIVE_CURRENT = 2.5 # bot in passive state current
ACTIVE_CURRENT = 13.25 # bot in activity current
OPERATION_VOLTAGE = 25 # operation voltage in volts
CAPACITY_COEFFICIENT = 1.8 # multiplier of maximal capacity according to maximum current

DISCHARGE_THRESHOLD = 0.1 # threshold capacity of discharge 
CHARGE_THRESHOLD = 0.9 # threshold capacity of charge

TEMPERATURE_STATE_NUMBER = 10 # number of discrete temperature states
IRRADIANCE_STATE_NUMBER = 20 # number of discrete irradiance states

BOT_ACTIVITY_BEGINNING = 6 # hour of bot activity beginning
BOT_ACTIVITY_FINISHING = 20 # hour of bot activity ending

KM_TO_CARBON_FOOTPRINT = 2.4 # kgCO_2 eq km for a truck of 20 tonnes
ENERGY_TO_FOOTPRINT = 0.175 * OPERATION_VOLTAGE # kgCO_2 eq Ah

MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # number of days per month

# kgCO_2 eq kWc for each country
PRODUCTION_COUNTRY_TO_FOOTPRINT = {
    "France": 355,
    "Germany": 416,
    "Mexico": 374,
    "Czech": 376,
    "Asia": 389
}

#kgCO_2 eq kWc for each material
PRODUCTION_MATERIAL_TO_FOOTPRINT = {
    "Monosillicium": 339,
    "Polysillicium": 480,
    "Thin": 300
}

# distance from France to the country of origin in km
PRODUCTION_COUNTRY_DISTANCE = {
    "France": 100,
    "Germany": 500,
    "Mexico": 7000,
    "Czech": 1000,
    "Asia": 9000
}
