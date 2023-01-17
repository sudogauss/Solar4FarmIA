import sys
from solar_activity import SolarActivity
from power_system import PowerSystem
from bot import Bot
from timer import Timer
import matplotlib.pyplot as plt


if __name__ == "__main__":
    n = len(sys.argv)
    if n != 3:
        print("You must provide epochs number, solar data file")
        print("Default example:")
        print("python3 main.py 1000 data/solar_data.csv")
        sys.exit(1)

    epochs = int(sys.argv[1])
    solar_data = sys.argv[2]

    solar_activity = SolarActivity(initial_state=(0.0, 0.0), solar_dataset=solar_data)
    bot = Bot(initial_probability=0.005,
              dp_winter=0.01,
              dp_spring=0.03,
              dp_summer=0.05,
              dp_fall=0.02)
    
    power_systems = []
    surfaces = []

    for s in range(3, 20, 1):
        surfaces.append(s)
        power_systems.append(PowerSystem(solar_area = s,
                                  solar_efficiency = 0.2,
                                  production_country = "France",
                                  max_power = s * 0.2 * 1000,
                                  material = "Monosillicium"))

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
        impacts[i] = power_systems[i].get_carbon_footprint() / 100

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    ax.set_xlabel("Carbon footprint (kgCO_2)")
    ax.set_ylabel("User efficiency(%)")
    ax.set_zlabel("Surface m^2")

    plt.plot(impacts, efficiencies, surfaces)

    plt.show()
    