# Solar4FarmIA

This project contains a [report](https://github.com/sudogauss/Solar4FarmIA/blob/main/docs/Alimentation%20de%20FarmBot%20et%20son%20impact%20carbone.pdf) describing an autonomous power system based on renewable solar energy and its carbon footprint. This report discusses a way to build this type of system, evaluates energy requirements of a smart agriculture bot(FarmBot), describes a way to simulate solar activity, bot's activity and power system behavior. It gives some formulas to calculate the carbon footprint of solar panels and all the power system.

## Code

The Solar4FarmIA folder contains the code simulating FarmBot(***bot.py***), Power system(***power_system.py***) and Solar activity(***solar_activity.py***). It also contains a ***timer.py*** iterator for the each-day-and-hour-of-the-year iteration. You can change consts in ***const.py*** to modify simulation parameters.

## Run

***Note: follow this steps only for Linux, use your own method to generate venv and run code for Windows.***

***Attention!!!: You must respect the right format of your csv data files. Take a look at the examples in data folder***

Clone the repository:

```bash
    $ git clone git@github.com:sudogauss/Solar4FarmIA.git
    $ cd Solar4FarmIA
```

Run the following commands to generate virtual environment and install all dependencies

```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
```

There is two simulations available: solar panel comparison ***(panel_simulation.py)*** and solar panel surface comparison ***(surface_simulation.py)***. Run:

```bash
    $ cd Solar4FarmIA
    $ python3 panel_simulation.py <epochs> \
    $ <solar_data_file.csv> <solar_panels.csv>
```

or

```bash
    $ cd Solar4FarmIA
    $ python3 surface_simulation.py <epochs> \
    $ <solar_data_file.csv>
```

Example for panel comparison simulation. You must open solar_panel.csv to see the corrseponding number of each solar panel:

```bash
    $ cd Solar4FarmIA
    $ python3 panel_simulation.py 20 data/solar_data.csv data/solar_panel.csv
```

Example for panel surface simulation:

```bash
    $ cd Solar4FarmIA
    $ python3 panel_simulation.py 20 data/solar_data.csv
```