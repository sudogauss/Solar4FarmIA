import sys
import pandas as pd
from solar_activity import SolarActivity
from power_system import PowerSystem
from bot import Bot
from timer import Timer
import matplotlib.pyplot as plt


if __name__ == "__main__":
    n = len(sys.argv)
    if n != 4:
        print("You must provide epochs number, solar data file and solar panel data file")
        print("Default example:")
        print("python3 main.py 1000 data/solar_data.csv data/solar_panel.csv")
        sys.exit(1)

    epochs = int(sys.argv[1])
    solar_data = sys.argv[2]
    solar_panel = sys.argv[3]

    solar_activity = SolarActivity(initial_state=(0.0, 0.0), solar_dataset=solar_data)
    bot = Bot(initial_probability=0.005,
              dp_winter=0.01,
              dp_spring=0.03,
              dp_summer=0.05,
              dp_fall=0.02)
    
    panel_df = pd.read_csv(solar_panel)
    power_systems = []

    for _, row in panel_df.iterrows():
        power_systems.append(PowerSystem(solar_area = float(row["Area"]),
                                  solar_efficiency = float(row["Efficiency"]),
                                  production_country = row["Origin"],
                                  max_power = int(row["Power"]),
                                  material = row["Material"]))

    m = len(power_systems)
    activities = [[0, 0] for _ in range(m)]
    impacts = [0.0 for _ in range(m)]

    for _ in range(epochs):
        for _t in Timer():
            if _t[2] <= 5 or _t[2] >= 9:
                continue
            solar_state = solar_activity.next_step(_t[2])
            bot_current = bot.next_step(_t[0], _t[2])
            for i, power_system in enumerate(power_systems):
                if power_system.next_step(bot_current, solar_state):
                    activities[i][0] += 1
                activities[i][1] += 1
        for i, power_system in enumerate(power_systems):
            power_system.reset()

    efficiencies = list(map(lambda x: (100 * x[0] / x[1]), activities))
    for i in range(m):
        impacts[i] = power_systems[i].get_carbon_footprint()

    plt.grid()
    plt.xlabel("Carbon footprint (kgCO_2)")
    plt.ylabel("User efficiency(%)")

    for i in range(m):
        plt.plot(impacts[i], efficiencies[i], marker="o", markersize=10)
        plt.text(impacts[i], efficiencies[i], str(i+1))

    plt.show()
    