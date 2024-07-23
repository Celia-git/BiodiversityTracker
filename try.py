import pandas as pd
import matplotlib.pyplot as plt

data = [["Bryce", 20, 25, 35],
        ["Big Bend", 2, 20, 300],
        ["Great Smoky", 5, 70, 204],
        ["Yellowstone", 1, 30, 201]]
 
# Form DataFrame from data
df = pd.DataFrame(data, columns=["Park Name", "Endangered", "Threatened", "Concern", "Recovery"])

df.plot(x="Park Name", y=["Endangered", "Threatened", "Concern"],
        kind="bar", figsize=(10, 10))
 
# Display plot
plt.show()
