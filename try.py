import pandas as pd
import matplotlib.pyplot as plt
import numpy

array = numpy.array(['Species of Concern', 'Endangered', 'Threatened', 'In Recovery'],
      dtype='<U18')



data = [["Bryce", 20, 25, 35, 100],
        ["Big Bend", 2, 20, 300, 150],
        ["Great Smoky", 5, 70, 204, 50],
        ["Yellowstone", 1, 30, 201, 75]]
 
# Form DataFrame from data
df = pd.DataFrame(data, columns=["Park Name", "Endangered", "Threatened", "Concern", "Recovery"])


df.plot(x="Park Name", y=["Endangered", "Threatened", "Concern", "Recovery"],
        kind="bar", figsize=(10, 10))
 
# Display plot
plt.show()
