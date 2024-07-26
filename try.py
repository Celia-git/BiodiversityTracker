import pandas as pd
import matplotlib.pyplot as plt
import numpy


data = [["Bryce", 20, 25, 35, 100],
        ["Big Bend", 2, 20, 300, 150],
        ["Great Smoky", 5, 70, 204, 50],
        ["Yellowstone", 1, 30, 201, 75]]
 
# Form DataFrame from data
df = pd.DataFrame(data, columns=["Park Name", "Endangered", "Threatened", "Concern", "Recovery"])


axes = df.plot(x="Park Name", y=["Endangered", "Threatened", "Concern", "Recovery"],
        kind="bar", figsize=(10, 10))


# ADD BAR LABELS
# DIVIDE INTO SUBPLOTS BY SPECIES TYPE

axes.tick_params(axis='x', labelrotation=0)
axes.set_ylabel("Recorded Observations")
axes.set_title("Observations of All Species by Conservation State at Each Participating Park")

ax = df.plot.bar(x="hello")

plt.show()

'''

animal_names = ['Lion', 'Gazelle', 'Cheetah']
mph_speed = [50, 60, 75]

fig, ax = plt.subplots()
bar_container = ax.bar(animal_names, mph_speed)
ax.set(ylabel='speed in MPH', title='Running speeds', ylim=(0, 80))
ax.bar_label(bar_container, fmt=lambda x: f'{x * 1.61:.1f} km/h')

plt.show()
'''