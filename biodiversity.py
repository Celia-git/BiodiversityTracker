from pandasql import sqldf
import numpy
import math
import warnings
import pandas as pd
import matplotlib.pyplot as plt # type: ignore
from sqlalchemy import create_engine

class Species():
    def __init__(self, scientific_name:str, common_name:str, category:str, conservation_status:str, park_sightings:list[tuple]):
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.category = category
        self.conservation_status = conservation_status
        self.park_sightings = park_sightings # List of tuples: (str park, int observations)

    # Return int amount of sightings at str Park for this Species 
    def get_sightings(self, park:str) -> int:
        for sighting in self.park_sightings:
            if sighting[0] == park:
                return sighting[1]
        return 0

    def __str__(self):
        sightings = ""
        for entry in self.park_sightings:
            sightings += "%s (%d)" % (entry[0], entry[1])
        return "%s: %s (%s) -%s | sightings: %s" % (self.common_name, self.scientific_name)
    


def get_connection():
    return create_engine(
        url="mysql+pymysql://root:D;09$7srO*);@127.0.0.1:3306/species"
    )

def create_data_frame(table_name, connection):
    return pd.read_sql_table(table_name, connection)

    
# Return Dictionary of park names and arrays of scientific_names: param: dataframe 
def sort_species_by_park(df):
    
    data = {}
    find_name_query = """SELECT scientific_name FROM df where park_name='%s'"""
    park_name_query = """SELECT park_name from df"""
    result = sqldf(park_name_query)
    for index, row in result.iterrows():
        park_name = row["park_name"]
        data[park_name] = sqldf(find_name_query % (park_name))
    return data
        
# Show graph based on dataframe: conservation level, amount of observations for all species, organized by park, subplots by category
def get_observations_by_conservation(obs_df, species_df):
    
    # Get pandas df of conservation status, scientific name 
    conservation_df = sqldf("""SELECT conservation_status, scientific_name FROM species_df WHERE NOT conservation_status=''""")
    
    # Get list of each park name and list of each conservation status
    all_parks = sqldf("""SELECT DISTINCT park_name FROM obs_df""").values.tolist()
    park_list = numpy.array(all_parks).ravel()
    all_cons = sqldf("""SELECT DISTINCT conservation_status FROM species_df WHERE NOT conservation_status='' AND NOT conservation_status='Species of Concern'""").values.tolist()
    all_cons = numpy.array(all_cons).ravel()
    
    # Get all categories of species, then combine vascular/nonvascular plants into one category
    categories = sqldf("""SELECT DISTINCT category FROM species_df WHERE NOT (category='Reptile' OR category='Amphibian')""").values.tolist()
    categories = numpy.array(categories).ravel()
    categories = categories[:-2]
    categories = numpy.append(categories, "Plant")
    labels = numpy.concatenate((all_cons[:0], ["Park Name"], all_cons[0:]))
    
    # Convert all_parks to 2D array with each park associated with 0 values for each conservation status
    for park in all_parks:
        park += [0] * len(all_cons)

    dataframes = dict(zip(categories, [0] * len(categories)))
    # Create a new dataframe for each category
    for category in categories:

        # Populate all_parks with amount of observations at each conservation level
        for park in all_parks:
            i = 1
            for cons in all_cons:
                
                names = sqldf(f"""SELECT scientific_name FROM species_df WHERE conservation_status='{cons}' AND category LIKE'%{category}%'""").values.tolist()
                names = numpy.array(names).ravel()
                # Add up observations for each of these names at each park
                total_observations = 0
                for name in names:
                    observations = sqldf("""SELECT observations FROM obs_df WHERE scientific_name='%s' and park_name='%s'""" % (name, park[0])).values.tolist()
                    observations = numpy.array(observations).ravel()
                    for o in observations:
                        total_observations += int(o)
                park[i] = total_observations
                i += 1

        df = pd.DataFrame(all_parks, columns=labels, index = park_list) 
        dataframes[category] = df

    # Plot the data
    row, col = (0, 0)
    fig, axes = plt.subplots(nrows=2, ncols=2)

    fig.suptitle("Observations of All Species by Conservation State and Park")

    # Plot the subplots
    for category in dataframes.keys():
        ax = axes[row, col]
        dataframes[category].plot(title=category, y= all_cons, kind="bar", ax=ax)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=-15)
        ax.set_xticklabels(park_list, fontsize=6)
        ax.set_ylabel("Observations")
        if col==1:
            row+=1
            col=0
        else:
            col += 1
    
    plt.show(block=True)


if __name__=="__main__":

    warnings.simplefilter(action='ignore', category=FutureWarning)


    try:
        engine = get_connection()
        print("Connection to 127.0.0.1 for root created successfully.")
        observations_df = create_data_frame("observations", engine)
        species_df = create_data_frame("species_info", engine)

    except Exception as ex:
        print("Connection could not be made due to : ", ex)

    get_observations_by_conservation(observations_df, species_df)
